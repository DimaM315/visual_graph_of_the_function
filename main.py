import pygame
import sys


from models import draw_axes
from GraphField import GraphField
from GraphMath import GraphMath

from settings import * 

pygame.init()


FONT_AXES = pygame.font.SysFont('comicsansms', 18)
# special font for a vertical serif
FONT_AXES_CHAIR_V = pygame.font.SysFont('comicsansms', 26)

size = (HEIGHT, WIDTH)
screen = pygame.display.set_mode(size)

field = GraphField(screen)
math_engine = GraphMath()


while True:
	screen.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# click on
			pass
	
	draw_axes(screen, FONT_AXES, FONT_AXES_CHAIR_V)
	field.draw_field()


	#seq = math_engine.sequence_gcd_counter()
	#point_list = math_engine.conver_seq_to_point_list(seq)
	point_list = math_engine.function_seq([(5, 0.5)])

	field.draw_points_list(point_list)
	
	pygame.display.update()