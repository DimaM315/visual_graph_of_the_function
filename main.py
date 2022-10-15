import pygame
import sys


from controllers import CompnsController
import mathCore
import snapshotController

from settings import HEIGHT, WIDTH, BLACK


# SHORTCUT:
# inp - input; div - division/"division value"; compn - componensts; 
# seq - sequencel; plch - placeholder; func - function;


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
func_polynomials = [
		[(-2, 2.5), (-1, 1), (0, -4)],
		[(-2, 1.3), (0, -5)]
	]
math_core = mathCore.MathCore(func_polynomials=func_polynomials, mode='func')
math_core.point_list = math_core.get_point_list()

page_controller = CompnsController(screen, compns_fonts, 
						increasing_px_x=math_core.increasing_px_x, 
						increasing_px_y=math_core.increasing_px_y)
snapshoter = snapshotController.SnapshoterGraph()



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
				
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if page_controller.func_inp_is_active():
					math_core.func_polynomials = page_controller.get_func_polynomials()
					math_core.mode = 'func'
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