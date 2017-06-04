#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time
import scipy as sp
import copy

numLEDs = 188
client = opc.Client('localhost:7890')

pixels_init=[ (100,100,100) ] * numLEDs

pixels=pixels_init

def reset_pixels(color,brightness=1):
    global pixels
    pixels=[tuple(brightness*c for c in color)]*numLEDs
    client.put_pixels(pixels)
    client.put_pixels(pixels)

def set_pixels(p0,def_pixels):
    global pixels
    pixels[p0:p0+len(def_pixels)]=def_pixels
    client.put_pixels(pixels)
    client.put_pixels(pixels)

def spot(pos,size,color):
    pixels=[(0,0,0)]*numLEDs
    xs=sp.linspace(-2,2,size)
    gradient=[sp.exp(-x**2/2)/sp.sqrt(2*sp.pi) for x in xs]
#    gradient=[g/2 for g in gradient]
    for i in range(len(gradient)):
        if( pos+size/2 < 127 ):
            pixels[ int(pos-(size-1)/2 + i) % 127 ] = tuple(int(v*gradient[i]) for v in color)
        else:
            pixels[ 127+int(size+pos-(size-1)/2 + i) % 61 ] = tuple(int(v*gradient[i]) for v in color) #to prevent weird edge effect on hexagon thing
#        pixels[ int(pos-(len(gradient)-1)/2 + i) % 61 ] = tuple(int(v*gradient[i]) for v in color)
#        print(int(pos-(len(gradient)-1)/2 + i) % numLEDs, tuple(v*gradient[i] for v in color))
    return pixels
    
def pixel_ave(l1,l2):
    l=[(0,0,0)]*len(l1) 
    for i in range(len(l1)):
        l[i]=tuple(int(sp.sum(z)) for z in zip(l1[i],l2[i])) #why does mean not work...
    return l

#colors
class colors:
    black=(0,0,0)
    white=(255,255,255)
    natural=(255, 197, 143)
    christmas=(255,195,120)
    warm_LED=(255, 210, 125)
    sodium=(255, 209, 178)
    dim_sodium=(255, 183, 130)
    cyan=(90, 210, 240)
    pink=(250,60,110)
    summer_sunset=[(248,177,149),(246,114,128),(192,108,132),(108,91,123),(53,92,125)]


#led arrangements
class arrangements:
    vaporwave=[colors.cyan]*127+[colors.pink]*61

class cfxn:
    def blues():
        return (100+sp.random.randint(90), 20+sp.random.randint(80), 155+sp.random.randint(100))
    
    def naturals():
        return (240+sp.random.randint(15), 182+sp.random.randint(15), 128+sp.random.randint(15))
    
    def reds():
        return (155+sp.random.randint(100), 20+sp.random.randint(80), 50+sp.random.randint(80))
    
    def random_color(color_range,offset=(0,0,0)):
        def rc():
            t=sp.random.randint(100)
            return (offset[0]+int(color_range[0]*sp.sin(sp.pi/30*t)),
                    offset[1]+int(color_range[1]*sp.sin(sp.pi/10*t)),
                    offset[2]+int(color_range[2]*sp.sin(sp.pi/20*t)))
        return rc
        
    def random_list_color(color_list):
        def rc():
            t=sp.random.randint(len(color_list))
            return color_list[t]
        return rc


#generrate ambient lights
def ambient_spots(p0,def_pixels,color_fcn,num_spots,spot_size,delay):
    spots=[spot(sp.random.randint(numLEDs),spot_size,color_fcn()) for i in range(num_spots)] 
    pixels_init[p0:p0+len(def_pixels)]=def_pixels
    t=0
    while True:
        t=(t+1) % num_spots
        pixels=pixels_init
        spots[t]=spot(p0+sp.random.randint(len(def_pixels)), spot_size, color_fcn() )
        for i in range(num_spots):
            pixels=pixel_ave(pixels,spots[i])
        client.put_pixels(pixels)
        time.sleep(delay) 

def ambient_fade(def_pixels,color_range,delay):
    pixels_init=def_pixels
    t=0
    while True:
        t=(t+1) % 100
        diff=(int(color_range[0]*sp.sin(2*sp.pi/100*t)),int(color_range[1]*sp.sin(2*sp.pi/30*t)),int(color_range[2]*sp.sin(2*sp.pi/60*t)))
        pixels=pixels_init
        for i in range(len(def_pixels)):
            pixels[i] = tuple(int(sp.sum(z)) for z in zip(pixels[i],diff))
        client.put_pixels(pixels)
        time.sleep(delay) 
        
def cycle_colors(color_list,delay):
    pixels_init=[(0,0,0)]*numLEDs
    t=0
    while True:
        t=(t+1)%len(color_list)
        t=sp.random.randint(len(color_list))
        pixels=pixels_init
        for i in range(numLEDs):
            pixels[i] = color_list[t]
        client.put_pixels(pixels)
        time.sleep(delay)

#vibes
class vibes:
    def summer(delay):
        bg=colors.summer_sunset[0]
        color_list=[(0,0,0)]*len(colors.summer_sunset)
        for i in range(len(colors.summer_sunset)):
            color_list[i]=tuple(x - y for x, y in zip(colors.summer_sunset[i], bg))
        ambient_spots(0,[bg]*numLEDs,cfxn.random_list_color(color_list),15,40,delay)
        
        
    def vaporwave(delay):
        ambient_spots(0,arrangements.vaporwave,cfxn.random_color((150,0,150),(50,0,50)),3,100,delay)
    
#nice blues with slightly purple backgrount
    #ambient_spots(0,[(180,60,220)]*numLEDs,blues,15,40,.5)

# random spots
# ambient_spots(0,[(110,110,110)]*numLEDs,random_color((80,80,80)),15,40,.5)

# random color
# ambient_spots(0,[black]*numLEDs,random_vapor,5,80,.5)


