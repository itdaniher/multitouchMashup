from multitouch import *

import Protoflo

import pygame
from pygame import draw, display, mouse
from pygame.locals import *
from numpy import *

try:
	protoflo = Protoflo.Protoflo()
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
			if pos.x < .33:
				protoflo.LED0.color[0] = int(pos.y*255)
			if .33 < pos.x < .66:
				protoflo.LED0.color[1] = int(pos.y*255)
			if pos.x > .66:
				protoflo.LED0.color[2] = int(pos.y*255)
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
				protoflo.LED0.color = 3*[0]
				protoflo.setLED0()
			break
	display.flip()
	if LED:
		protoflo.setLED0()
stop_multitouch(devs)
