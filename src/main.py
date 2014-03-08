#!/usr/bin/env python2.7

from PIL import Image
from iris_detection import detect_iris

def show(filename):
    im = Image.open(filename)
    im.show()

if __name__ == '__main__':
    print "[*] irismatch Enconding"
    filename = "../working-db/003R_3.png"
    #show(filename)
    detect_iris(filename)
    

