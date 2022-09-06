import pygame
import sys


from controllers import CompnsController
from MathCore import MathCore

from settings import HEIGHT, WIDTH, BLACK


# SHORTCUT:
# inp - input; div - division/"division value"; compn - componensts; 
# seq - sequencel; plch - placeholder; func - function;


pygame.init()


compns_fonts = {
	'axes' : pygame.font.SysFont('comicsansms', 18),
	# special font for a vertical serif
	'axes_chair_y' :  pygame.font.SysFont('comicsansms', 26),
	'inputbox' : pygame.font.Font(None, 32)
}

size = (HEIGHT, WIDTH)
screen = pygame.display.set_mode(size)


# app components
math_core = MathCore(func_polynomials=[(3, 0.5)], mode='seq')

page_controller = CompnsController(screen, compns_fonts, 
						increasing_px_x=math_core.increasing_px_x, 
						increasing_px_y=math_core.increasing_px_y)



while True:
	screen.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# click on
			pass
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if page_controller.func_inp_is_active():
					math_core.func_polynomials = page_controller.get_func_polynomials()
					math_core.mode = 'func'
				
				if page_controller.inp_div_x_is_active():
					new_increasing_x = page_controller.get_new_increasing(axic='x')
					math_core.increasing_px_x = new_increasing_x
					if math_core.mode != 'seq':
						page_controller.increasing_px_x = new_increasing_x
				
				if page_controller.inp_div_y_is_active():
					new_increasing_y = page_controller.get_new_increasing(axic='y')
					math_core.increasing_px_y = new_increasing_y
					if math_core.mode != 'seq':
						page_controller.increasing_px_y = new_increasing_y

		page_controller.handle_event(event)
		
	page_controller.render_compns()

	point_list = math_core.get_point_list()
	page_controller.field_controller.draw_points_list(point_list)
	
	pygame.display.update()