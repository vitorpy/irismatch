#!/usr/bin/env python2.7

from PIL import Image, ImageFilter
from iris_detection import detect_iris
from scipy.ndimage import filters
import matplotlib.pyplot as plt
from scipy.misc import toimage

def show(filename):
    im = Image.open(filename)
    im.show()

def edge_detect_experiment(filename):
    raw_image = plt.imread(filename)
    raw_image = raw_image[:,:,0] # get the first channel

    #plt.imshow(raw_image)
    #plt.show()

    #image = filters.sobel(raw_image, 0)**2 + filters.sobel(raw_image, 1)**2
    image = toimage(raw_image)
    image = image.filter(ImageFilter.FIND_EDGES)

    image.show()

    #plt.imshow(image)
    #plt.show()    

if __name__ == '__main__':
    print "[*] irismatch Enconding"
    filename = "../working-db/003R_3.png"
    
    edge_detect_experiment(filename)
    
    #show(filename)
    #detect_iris(filename)
    

