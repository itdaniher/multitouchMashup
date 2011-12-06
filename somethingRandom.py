from multitouch import *
import bitarray

import Protoflo

import pygame
from pygame import draw, display, mouse
from pygame.locals import *
from numpy import *

try:
	protoflo = Protoflo.Protoflo()
	LED = True
except:
	LED = False

pygame.init()

devs = init_multitouch(touch_callback)
flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
mode = max(display.list_modes(0, flags))
display.set_mode(mode, flags)
screen = display.get_surface()
width, height = screen.get_size()

mouse.set_visible(False)

fingers = []

while True:
	if touches:
		frame, timestamp, fingers = touches.pop()

	screen.fill((0xef, 0xef, 0xef))

	prev = None
	for i, finger in enumerate(fingers):
		pos = finger.normalized.position
		vel = finger.normalized.velocity

		x = int(pos.x * width)
		y = int((1 - pos.y) * height)
		p = (x, y)
		r = int(finger.size * 10)

		if prev:
			draw.circle(screen, 0, prev[0], prev[1], 0)
		prev = p, r

		draw.circle(screen, 0, p, r, 0)
		vx = vel.x
		vy = -vel.y
		posvx = x + vx / 10 * width
		posvy = y + vy / 10 * height
		if LED:
			if pos.x < .25:
				protoflo.LED0.color[0] = int(pos.y*255)
			if .25 < pos.x < .5:
				protoflo.LED0.color[1] = int(pos.y*255)
			if .5 < pos.x < .75:
				protoflo.LED0.color[2] = int(pos.y*255)
			if pos.x > .75:
				protoflo.otherLEDs = bitarray.bitarray(6*[0], endian="little")
				protoflo.otherLEDs[int(pos.y*6)] = 1
		draw.line(screen, 0, p, (posvx, posvy))

	if len(fingers) == 4:
		n_still = 0
		n_down = 0
		n_up = 0
		for i, finger in enumerate(fingers):
			vel = finger.normalized.velocity
			t = 0.5
			if -t <= vel.x < t and -t <= vel.y < t:
				n_still += 1
			elif -2 <= vel.x < 2 and vel.y < -4:
				n_down += 1
			elif -2 <= vel.x <2  and vel.y > 4:
				n_up += 1
		if n_still == 1 and n_down == 3:
			if LED:
				protoflo.otherLEDs = bitarray.bitarray(6*[0], endian="little")
				protoflo.LED0.color = 3*[0]
				protoflo.setLEDs()
			break
	display.flip()
	if LED:
		protoflo.setLEDs()
stop_multitouch(devs)
