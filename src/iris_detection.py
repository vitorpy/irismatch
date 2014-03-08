#!/usr/bin/env python2.7

# Imported from https://gitorious.org/hough-circular-transform
# License: GPLv3
# Date: Fri, Mar 7 2014

import matplotlib.pyplot as plt
import matplotlib.patches as plt_patches
import houghcirculartransform as hct
import numpy as np

def detect_iris(filename):
    """
   Example function call:
       For a trickier example, load 'test2.png'!
       (Can't fint the circle? Try the debug mode!)
       ((Pro tip: try lowering the threshold...))
    """
    CH = hct.CircularHough()

    raw_image = plt.imread(filename)
    raw_image = raw_image[:,:,0] # get the first channel
    print "[DEBUG] Image shape is: " + str(raw_image.shape)

    min_size = min(raw_image.shape)
    # 0.1 to 0.8 from Daugman paper
    lower_bound = int(0.1 * min_size) / 2
    upper_bound = int(0.8 * min_size) / 2
    accumulator, radii = CH(raw_image, radii=np.arange(lower_bound, upper_bound, 3), threshold=0.01, binary=True, method='fft')
    
    print "[DEBUG] Calling imshow"
    plt.imshow(raw_image)

    plt.title('Raw image (inverted)')

    # Add appropriate circular patch to figure (thanks to MZ!):
    for i, r in enumerate(radii):
        # [Vitor] where i is the accumulator index and r is the radius
        # accumulator a list of points
        point = np.unravel_index(accumulator[i].argmax(), accumulator[i].shape)
        try:
            blob_circ = plt_patches.Circle((point[1], point[0]), r, fill=False, ec='red')
            plt.gca().add_patch(blob_circ)
        except ValueError:
            print point, r
            continue
    # Fix axis distortion:
    plt.axis('image')

    plt.show()

if __name__ == '__main__':
    detect_iris("../working-db/003L_3.png")
    
