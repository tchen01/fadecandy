#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

numLEDs = 60
client = opc.Client('localhost:7890')

while True:
	for i in range(numLEDs):
		pixels = [ (80,0,80) ] * numLEDs
		pixels[i] = (255, 0, 255)
#		pixels[int(i+numLEDs/2)%numLEDs] = (255, 0, 255)
		client.put_pixels(pixels)
		time.sleep(0.04)
