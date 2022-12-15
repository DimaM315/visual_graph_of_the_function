import pygame
import sys

from services import ComponentsController, SnapshoterGraph
from settings import WINDOW_SIZE, BLACK
from entity_types import GraphTypes


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

	screen = pygame.display.set_mode(WINDOW_SIZE)

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
					snapshoter.create_black_white_snapshot(math_core.coords_list)
				elif page_controller.btn_add_overlay.on_the_element(event):
					page_controller.btn_add_overlay.change_active()
				
				elif page_controller.btn_add_grid.on_the_element(event):
					page_controller.field_controller.toggle_field_grid()
					page_controller.btn_add_grid.change_active()
				
				elif page_controller.btn_set_sinusoid.on_the_element(event):
					_set_new_sinusoid(page_controller, math_core)

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if page_controller.func_inp_is_active():
						# User entered new function.
						_set_new_function(page_controller, math_core)		
					elif page_controller.inp_div_x_is_active():
						# User entered new incr x.
						_change_increasing_x(page_controller, math_core)
					elif page_controller.inp_div_y_is_active():
						# User entered new incr y.
						_change_increasing_y(page_controller, math_core)
					
					elif page_controller.inp_phase_is_active():
						_change_sinusoid_phase(page_controller, math_core)
					elif page_controller.inp_ampl_is_active():
						_change_sinusoid_ampl(page_controller, math_core)
						
			page_controller.handle_event(event)
			
		page_controller.render_compns()
		page_controller.field_controller.draw_coords_list(math_core.coords_list)
		
		pygame.display.update()


def _change_sinusoid_ampl(pc:ComponentsController, math_core):
	new_ampl = pc.get_sinusoid_ampl()
	math_core.set_sinusoid_params(new_ampl=new_ampl)
	_update_coords_list(pc, math_core)

def _change_sinusoid_phase(pc:ComponentsController, math_core):
	new_phase_kf = pc.get_sinusoid_phase()
	math_core.set_sinusoid_params(phase_kf=new_phase_kf)
	_update_coords_list(pc, math_core)


def _change_increasing_x(pc:ComponentsController, math_core):
	new_incr_x = pc.get_new_increasing(axic='x')
	math_core.increasing_px_x = new_incr_x
	pc.increasing_px_x = new_incr_x
	_update_coords_list(pc, math_core)

def _change_increasing_y(pc:ComponentsController, math_core):
	new_incr_y = pc.get_new_increasing(axic='y')
	math_core.increasing_px_y = new_incr_y
	pc.increasing_px_y = new_incr_y
	_update_coords_list(pc, math_core)

def _set_new_function(pc:ComponentsController, math_core):
	math_core.set_tmp_func(pc.get_func_polynomials())
	math_core.mode = GraphTypes.FUNC
	_update_coords_list(pc, math_core)


def _set_new_sinusoid(pc:ComponentsController, math_core):
	new_phase_kf = pc.get_sinusoid_phase()
	new_ampl = pc.get_sinusoid_ampl()

	math_core.set_sinusoid_params(phase_kf=new_phase_kf, new_ampl=new_ampl)
	math_core.mode = GraphTypes.SINUSOID
	_update_coords_list(pc, math_core)
	

def _update_coords_list(pc:ComponentsController, math_core):
	if pc.add_graphic_btn_is_active():
		# Don`t revome data of old graphic.
		math_core.coords_list += math_core.get_coords_list()
	else:
		# Refresh data of old graphic.
		math_core.coords_list = math_core.get_coords_list()