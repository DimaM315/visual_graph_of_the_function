import pygame
import sys


from controllers import ConponenstsController
from GraphMath import GraphMath

from settings import * 

pygame.init()


components_fonts = {
	'axes' : pygame.font.SysFont('comicsansms', 18),
	# special font for a vertical serif
	'axes_chair_y' :  pygame.font.SysFont('comicsansms', 26),
	'inputbox' : pygame.font.Font(None, 32)
}

size = (HEIGHT, WIDTH)
screen = pygame.display.set_mode(size)


# app components
math_engine = GraphMath(func_polynomials=[(3, 0.5)], mode='seq')
math_engine.sequence = math_engine.sequence_divisor_counter()

page_controller = ConponenstsController(screen, components_fonts, 
						increasing_px_x=math_engine.increasing_px_x, 
						increasing_px_y=math_engine.increasing_px_y)



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
				if page_controller.function_inputbox_is_active():
					math_engine.func_polynomials = page_controller.get_func_polynomials()
					math_engine.mode = 'func'
				
				if page_controller.input_division_value_x_is_active():
					new_increasing_x = page_controller.get_new_increasing(axic='x')
					math_engine.increasing_px_x = new_increasing_x
					page_controller.increasing_px_x = new_increasing_x
				
				if page_controller.input_division_value_y_is_active():
					new_increasing_y = page_controller.get_new_increasing(axic='y')
					math_engine.increasing_px_y = new_increasing_y
					page_controller.increasing_px_y = new_increasing_y

		page_controller.handle_event(event)
		
	page_controller.render_components()

	point_list = math_engine.get_point_list()

	page_controller.field_controller.draw_points_list(point_list)
	
	pygame.display.update()