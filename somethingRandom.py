from multitouch import *

import pygame
from pygame import draw, display, mouse
from pygame.locals import *
from numpy import *

pygame.init()

devs = init_multitouch(touch_callback)

flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
mode = max(display.list_modes(0, flags))
#display.set_mode(mode, flags)
display.set_mode((640, 480))
screen = display.get_surface()
width, height = screen.get_size()

mouse.set_visible(False)

fingers = []

while True:
	if touches:
		frame, timestamp, fingers = touches.pop()

	#print frame, timestamp
	screen.fill((0xef, 0xef, 0xef))

	prev = None
	for i, finger in enumerate(fingers):
		pos = finger.normalized.position
		vel = finger.normalized.velocity

		x = int(pos.x * width)
		y = int((1 - pos.y) * height)
		p = (x, y)
		r = int(finger.size * 10)
		#print "finger", i, "at", (x, y)
		#xofs = int(finger.minor_axis / 2)
		#yofs = int(finger.major_axis / 2)

		if prev:
			draw.line(screen, (0xd0, 0xd0, 0xd0), p, prev[0], 3)
			draw.circle(screen, 0, prev[0], prev[1], 0)
		prev = p, r

		draw.circle(screen, 0, p, r, 0)
		#draw.ellipse(screen, 0, (x - xofs, y - yofs, xofs * 2, yofs * 2))

		#sa[int(pos.x * n_samples)] = int(-32768 + pos.y * 65536)

		vx = vel.x
		vy = -vel.y
		posvx = x + vx / 10 * width
		posvy = y + vy / 10 * height
		draw.line(screen, 0, p, (posvx, posvy))

	# EXIT! One finger still, four motioning quickly downward.
	if len(fingers) == 3:
		n_still = 0
		n_down = 0
		n_up = 0
		for i, finger in enumerate(fingers):
			vel = finger.normalized.velocity
			#print i, "%.2f, %.2f" % (vel.x, vel.y)
			t = 0.5
			if -t <= vel.x < t and -t <= vel.y < t:
				n_still += 1
			elif -2 <= vel.x < 2 and vel.y < -4:
				n_down += 1
			elif -2 <= vel.x <2  and vel.y > 4:
				n_up += 1
		if n_still == 1 and n_down == 2:
			break
		if n_still == 1 and n_up == 2:
			print 'up up and away'
			flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
			mode = max(display.list_modes(0, flags))
			display.set_mode(mode, flags)
			width, height = screen.get_size()

	display.flip()

stop_multitouch(devs)
