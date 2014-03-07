# Imported from https://gitorious.org/hough-circular-transform
# License: GPLv3
# Date: Fri, Mar 7 2014

import numpy as np
from scipy.signal import fftconvolve, convolve2d, correlate2d
from scipy.ndimage import filters
from warnings import warn

class CircularHough(object):
    def __init__(self, radii=None, threshold=None, 
                 binary=None, stencilwidth=None):
        self.radii = radii
        self._threshold = threshold
        self._binary = binary
        self._stencilwidth=stencilwidth
        self.edge_list = []
       
    def __call__(self, image, radii=np.array([20]), method='fft', 
                 threshold=0.5, edgefilter="sobel", binary=False, stencilwidth=1):
        """ Performs the Circular Hough Transform (CHT) on the supplied image.
        
            I calculate the CHT for a range of circualr radii, or for just a
            single radius: what ever 1d array of radii you throw my way. 
    
            I can also perform edge detection using a variety of algorithms 
            for you and make the working copy binary, however, I will not 
            otherwise pre-process (read: noise reduction, e.g. Gaussian 
            smoothing). If you worry about these issues, use 'debug' as method
            to just return the edge-filtered image and a quality number, which
            should be << 1.

            The methods I provide for the CHT are an 'explicit' and an 'fft'
            method. The latter is based on the fft representation of the 
            convolution with a circular kernel, whereas the former uses the
            fact that the processed image -- after edge detection etc. -- is 
            'sparse' (i.e. low density of non-zero values). I _think_ they may 
            be equivalent, but I haven't done the maths. They should both do 
            the trick, but the explicit method is faster for sparse images and
            horribly slow for dense, whereas the fft-method doesn't really 
            care about such trivial matters. Which is the faster? Probably
            'fft'...

            Since checking many radii can be pretty slow, the choice of radii is
            accompanied by a stencil widthoption, which makes the circular stencil 
            coarser, and hence less precise, but which may allow wider steps in
            radius, if stencilwidth of the same order as the increment between
            radii. This could, for instance, be used in an iterative method.

            If the r-interval has been chosen appropriately, the returned 
            3D accumulator should hava maximum at or around a point 
            corresponding to the centre coordinates and radius fitting best to 
            the signal. Sort of. Please ask...
        """
        
        self.__init__(radii, threshold, binary, stencilwidth)

        if self._assert_sanity(min(image.shape)):
            temp_image = self._find_edges(image, edgefilter)

            self.edge_list = np.array(temp_image.nonzero())
            self.density = float(self.edge_list[0].size)/temp_image.size
            print "Singal density:", self.density
            if self.density > 0.25:
                warn("High density! Consider preprocessing more agressively!")
        
            if method.lower() == "fft":
                return self._fft_Hough(temp_image)
            elif method.lower() == "explicit":
                return self._explicit_Hough(temp_image)
            elif method.lower() == "debug":
                return temp_image, self.density
            else:
                print "Unknown method:", method, "Try 'fft' or 'explicit'!"
                return -1
        else:
            warn("Something was wonky with the arguments you sent me...") # warn or error?
            return -1

    def _assert_sanity(self, max_diameter): 
        """ This is an incredibly crude method, that performs sanity checks
            on the parameters supplied in the function call. """
        
        n_errors = 0
        r_max = self.radii.max()
        r_min = self.radii.min()

        if 2*r_max >= max_diameter:
            print "Please keep 2*r_max < the image dimensions!"
            n_errors += 1

        if r_min < 1:
            print "Please keep r_min > 1!"
            n_errors += 1
        
        if self._threshold == 0 or self._threshold == 1:
            print "Please keep threshold strictly between 0 and 1!"
            n_errors += 1

        if n_errors > 0:
            print n_errors, "errors detected in config. You can do better!"

        return n_errors == 0

    def _explicit_Hough(self, image):
        """ This is the explicit straightforward version of the CHT, whose 
            application relies on having pre-processed the image approrpiately,
            removing noise through smoothing and thresholding. Usually slow."""

        print "Using explicit method..."
        warn("Warning! This is probably slower than 'fft'!")

        radii = self.radii
        r_max = radii.max()
        acc = np.zeros( (radii.size, 2*r_max + image.shape[0], 
                                     2*r_max + image.shape[1]) )
        for i, r in enumerate(radii):
            C = self._get_circle(r, self._stencilwidth)
            for en in xrange(self.edge_list.shape[1]):
                e = self.edge_list[:, en]
                acc[i, e[0]+r_max-r : e[0]+r_max+r+1, e[1]+r_max-r:e[1]+r_max+r+1] += \
                    C*image[e[0], e[1]] #Needschecking!
        
        return acc[:, r_max : -r_max, r_max : -r_max], radii #Needschecking!
            
    def _fft_Hough(self, image):
        """ This is the fft based convolution version of the CHT, which may be 
            more efficient if the data hasn't been sufficiently smoothed and 
            otherwise pre-processed... """

        print "Using fft-method..."

        radii = self.radii
        acc = np.zeros( (radii.size, image.shape[0], image.shape[1]) )

        for i, r in enumerate(radii):
            C = self._get_circle(r, self._stencilwidth)
            acc[i,:,:] = fftconvolve(image, C, 'same')
    
        return acc, radii

    def _get_circle(self, r, w=1):
        """ Returns a circular kernel/stencil with the specified radius. """

        if w > r:
            print "Dude! Width of annulus can't be > radius! (Using r...)"
            w = r

        grids = np.mgrid[-r:r+1, -r:r+1]
        template = grids[0]**2 + grids[1]**2
        large_circle = template <= r**2
        large_circle.dtype = np.int8
        small_circle = template < (r - w)**2
        small_circle.dtype = np.int8
        
        return large_circle - small_circle

    def _find_edges(self, image, edge_filter):
        """ Method for handling selection of edge_filter and some more
            pre-processing. """

        if edge_filter.lower() == "sobel":
            print "Using Sobel-filter for edge detection."
            image = filters.sobel(image, 0)**2 + filters.sobel(image, 1)**2 
        elif edge_filter.lower() == "canny":
            print "Using Canny-filter for edge detection."
            print "Actually... no... Couldn't find it." # use warn..?
            #image = filters.canny(image)
            print "Using Sobel-filter for edge detection.!"
            image = filters.sobel(image, 0)**2 + filters.sobel(image, 1)**2 
        elif edge_filter is None:
            print "I sure hope you've done your own edge detection..."
        else:
            print "Unknonw option:", edge_filter, "Try: 'sobel', 'canny' or None!"
            print "I sure hope you've done your own edge detection..."

        image -= image.min()

        if self._binary:
            image = image > image.max()*self._threshold
            image.dtype = np.int8
        elif self._threshold > 0:
            image = np.where(image > image.max()*self._threshold, image, 0)
        
        return image 
        
