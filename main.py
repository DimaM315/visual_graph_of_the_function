import pygame
import sys

from services import ComponentsController, SnapshoterGraph
from settings import HEIGHT, WIDTH, BLACK


# SHORTCUT:
# inp - input; div - division/"division value"; compn - componensts; 
# seq - sequencel; plch - placeholder; func - function;

def app(math_core):
	pygame.init()

	compns_fonts = {
		'axes' : pygame.font.SysFont('comicsansms', 18),
		# special font for a vertical serif
		'axes_chair_y' :  pygame.font.SysFont('comicsansms', 26),
		'inputbox' : pygame.font.Font(None, 32),
		'inputbox_func' : pygame.font.Font(None, 18),
		'btn': pygame.font.Font(None, 19),

	}

	size = (HEIGHT, WIDTH)
	screen = pygame.display.set_mode(size)


	# app components
	page_controller = ComponentsController(screen, compns_fonts, 
							increasing_px_x=math_core.increasing_px_x, 
							increasing_px_y=math_core.increasing_px_y)
	snapshoter = SnapshoterGraph()


	while True:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				# click on
				if page_controller.btn_snapshoter.on_the_element(event):
					snapshoter.create_black_white_snapshot(math_core.point_list)
				elif page_controller.btn_add_overlay.on_the_element(event):
					page_controller.btn_add_overlay.change_active()
					print("Add overlay change status")
				elif page_controller.btn_add_grid.on_the_element(event):
					page_controller.field_controller.draw_field_grid()
					page_controller.btn_add_grid.change_active()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if page_controller.func_inp_is_active():
						# User rentered new function.
						math_core.set_func_polynomials(page_controller.get_func_polynomials())
						math_core.mode = 'func'
						if page_controller.add_graphic_btn_is_active():
							# Don`t revome data of old graphic.
							math_core.point_list += math_core.get_point_list()
						else:
							# Refresh data of old graphic.
							math_core.point_list = math_core.get_point_list()
					
					if page_controller.inp_div_x_is_active():
						new_increasing_x = page_controller.get_new_increasing(axic='x')
						math_core.increasing_px_x = new_increasing_x
						page_controller.increasing_px_x = new_increasing_x
						math_core.point_list = math_core.get_point_list()
					
					if page_controller.inp_div_y_is_active():
						new_increasing_y = page_controller.get_new_increasing(axic='y')
						math_core.increasing_px_y = new_increasing_y
						page_controller.increasing_px_y = new_increasing_y
						math_core.point_list = math_core.get_point_list()
						
			page_controller.handle_event(event)
			
		page_controller.render_compns()

		page_controller.field_controller.draw_points_list(math_core.point_list)
		
		pygame.display.update()