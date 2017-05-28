#!/usr/bin/env python

# Open Pixel Control client: All lights to solid white

import opc, time

numLEDs = 64
client = opc.Client('localhost:7890')

black = [ (0,0,0) ] * numLEDs
white = [ (180,0,180) ] * numLEDs

while True:
    client.put_pixels(white)
    time.sleep(0.1) 
    client.put_pixels(black)
    time.sleep(0.1)
