"""JEM Playing Around With RGB<->HSI<->RGBW conversion formulas"""
""" Butchered the original color.py module to do this work, please do not consider this as production useful"""

import colorsys
import math
import numpy as np
from copy import deepcopy

__all__=['RGB', 'HSV', 'Hex', 'Color', 'RGBW']

#https://blog.saikoled.com/post/44677718712/how-to-convert-from-hsi-to-rgb-white
def D_calc_white_via_hsi():
    pass


#this
#https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

#https://stackoverflow.com/questions/40312216/converting-rgb-to-rgbw   
def C_calc_white_from_rgb(r,g,b):
    pass

def B_calc_white_from_rgb(r,g,b):
    M = float(max(r,g,b))
    m = float(min(r,g,b))
    Wo = 0
    if M == 0.0 and m == 0.0:
        pass
    else:
        if float(m)/float(M) < 0.5:
            Wo = ((m*M)/ (M-m))
        else:
            Wo = M
    Q = 255
    K = (Wo+M) / m
    Ro = floor(  ( (K * float(r))  - Wo) / Q)
    Go = floor(  ( (K * float(g))  - Wo) / Q)
    Bo = floor(  ( (K * float(b))  - Wo) / Q)
    return(Ro,Go,Bo,Wo)
#https://2sn.org/python/color.py


def constrain(val, min, max):
    ret = val
    if val <= min:
        ret = min
    if val >= max:
        ret=max
    return ret


def is_hsv_tuple(hsv):
    "check that a tuple contains 3 values between 0.0 and 1.0"
    return len(hsv) == 4 and all([(0.0 <= t <= 1.0) for t in hsv[0:3]])

def is_rgb_tuple(rgb):
    "check that a tuple contains 3 values between 0 and 255"
    return len(rgb) == 4 and all([(0 <= t <= 255) for t in rgb])

def is_rgbw_tuple(rgbw):
    "check for valid RGBW tuple"
    return len(rgbw) == 4 and all([(0 <= t <= 255) for t in rgbw])



def test_rgb2hsi2rgb(r,g,b):
    (h,s,i) = rgb2hsi(r,g,b)
    print("ORIGRGB: {0} / {1} / {2} ||| HSI: {3} / {4} / {5} ".format(r,g,b,h,s,i))
    (rr,gg,bb) = hsi2rgb(h,s,i)
    print("CONV RGB: {0} / {1} / {2} ||| HSI: {3} / {4} / {5} ".format(rr,gg,bb,h,s,i))



def rgb_hsi_tests():
    colors = {
        'white' : ((1,1,1),(1.0,1.0,1.0)),
        'olive' : ((.75,.75,0),(60.0,1.0,.5)), #okk
        'teal' : ((.5,1.0,1.0),(180.0,.4,.833)), #ok
        'purple' : ((.75,.25,.75),(300.0, .571, .583)), #ok
        'blue2' : ((.255,.104, .918),(251.1,.756,.426)), #ok
        'green2': ((.116,.675,.255),(134.9, .667, .349)), # ok
        'orange' : ((.931,.463,.316),(14.3, .446, .570)), #ok
        'yellow' : ((.998,.974,.532),(56.9, .363 ,.835)), #ok
        'dusty_blue' : ((.495,.493,.721),(240.5, .135, .570 )), #ok
        'dark' : ((0.0,0.0,0.0),(0.0,0.0,0.0))
        }
    for i in colors:
        print(i)
        r,g,b = colors[i][0]
        R = r*255.0
        G = g*255.0
        B = b*255.0
        
        (h,s,i) = colors[i][1]
        (H2,S2,I2) = rgb2hsi(R,G,B)
        print("EXPECTED:: R: {0} / G: {1} / B: {2} || H: {3} / S: {4} / I: {5}".format(R,G,B,h,s,i))
        print("Calculated: ..........................................h= {0} / s= {1} / i  {2}".format(round(H2,4),round(S2,4),round(I2,4)))

def  hsi2rgb(h,s,i):
    h = constrain(float(h), 0.0,1.0)
    s = constrain(float(s), 0.0,1.0)
    i = constrain(float(i), 0.0,1.0)
    x = 0.0
    y = 0.0
    z = 0.0
    r = 0.0
    g = 0.0
    b = 0.0
    
    x = i * (1.0-s)
    if h < (2.0 * math.pi/3.0):
        y = i  *( 1.0 + (s * math.cos(h)) /  (math.cos(math.pi/3.0 - h)))
        z = 3.0 * i - (x + y)
        b  = x
        r = y
        g = z
    elif h < (4.0*math.pi/3.0):
        y = i * (1.0 + (s * math.cos(h - 2.0 * math.pi / 3.0)) / (math.cos(math.pi/3.0 - (h- 2.0 * math.pi/3.0))))
        z = 3.0 * i - (x+y)
        r = x
        g = y
        b = z
    else:
        y = i * (1.0 + (s * math.cos(h-4.0 * math.pi / 3.0)) / (math.cos(math.pi / 3.0 - (h - 4.0 * math.pi / 3.0))))
        z = 3.0 * i - (x+y)
        r = z
        g = x
        b = y
    return(r*255,g*255,b*255)



#https://en.wikipedia.org/wiki/HSL_and_HSV#Saturation                                                           
def rgb2hsi(red,green,blue):
    r = constrain(float(red)/255.0,0.0,1.0)
    g = constrain(float(green)/255.0, 0.0,1.0)
    b = constrain(float(blue)/255.0,0.0,1.0)
    intensity = 0.33333*(r+g+b)

    M = max(r,g,b)
    m = min(r,g,b) 
    C = M - m

    saturation = 0.0
    if intensity == 0.0:
        saturation = 0.0
    else:
        saturation = (1-(m/intensity))

    hue = 0
    if M == m:
        hue = 0
    if M == r:
        print("A",M,m)
        if M == m:
            hue = 0.0
        else:
            hue = 60.0* (0.0 + ((g-b) / (M-m)))
    if M == g:
        print("B")
        if M == m:
            hue = 0.0
        else:
            hue = 60.0* (2.0 + ((b-r) / (M-m)))
    if M == b:
        print("C")
        if M == m:
            hue = 0.0
        else:
            hue = 60.0 * (4.0 + ((r-g) / (M-m)))
    if hue < 0.0:
        print("D")
        hue = hue + 360

    return(hue,abs(saturation),intensity)



            
def HSI(h,s,i):
    return Color(0,0,0,0)


def RGBW(r,g,b,w):
    "Create new RGBW Color"
    t = (r,g,b,w)
    assert is_rgbw_tuple(t)
    return(Color(t))

def RGB(r,g,b):
    "Create a new RGB color"
    return Color(hsi2rgbw(rgb2hsi(r,g,b)))



def Hex(value):
    "Create a new Color from a hex string"
    value = value.lstrip('#')
    lv = len(value)
    rgb_t = (int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    r = rgb_t.next()
    g = rgb_t.next()
    b = rgb_t.next()
    return (r,g,b)


class Color(object):

    def __init__(self, rgbw_tuple):
#        from IPython import embed; embed()   
        print(rgbw_tuple)
        self.rgbw = rgbw_tuple


    def copy(self):
        return deepcopy(self)



    def rgbw(self):
        "returns a rgbw[0-255] tuple"
        return self.rgbw



    """
    Properties representing individual RGBW components
    """
    @property
    def r(self):
        return self.rgbw[0]

    @r.setter
    def r(self, val):
        self.rgbw[0] = val

    @property
    def g(self):
        return self.rgbw[1]

    @g.setter
    def g(self, val):
        self.rgbw[1] = val

    @property
    def b(self):
        return self.rgbw[2]

    @b.setter
    def b(self, val):
        self.rgbw[2] = val

    @property
    def w(self):
        return rgbw[3]

    @w.setter
    def w(self,val):
        self.rgbw[3] = val

    
         
        
if __name__=='__main__':
    import doctest
    doctest.testmod()
