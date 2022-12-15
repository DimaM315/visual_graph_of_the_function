from settings import *
from models import function_transform, check_correct_func_polynom
from entity_types import GraphTypes, Polynom, FunctionRepr


from services.viewController.widgets import InputBox, Button
from services.viewController.graphField import GraphFieldController


class ComponentsController:
	# Initialize and maintain other components: axic, inputboxes, text.
	# In other words, the class controls any entity except for the field

	def __init__(self, screen, fonts:dict, increasing_px_x:int, increasing_px_y:int):
		# :fonts - dict of necessary fonts for initialize some components
		self.sc = screen
		self.fonts = fonts

		
		self.increasing_px_x = increasing_px_x
		self.increasing_px_y = increasing_px_y

		self.field_controller = GraphFieldController(self.sc, self.fonts['axes'], self.fonts['axes_chair_y'])

		self.input_function_box = InputBox(
					50, HEIGHT-60, 140, 32, pg_font=self.fonts['inputbox_func'], plch=INP_FUNC_PLCH,
					allowed_chars=ALLOWED_CHARS_LIST)
		self.input_division_value_x = InputBox(
					50, HEIGHT-100, 140, 32, pg_font=self.fonts['inputbox'], plch=INP_DIV_X_PLCH)
		self.input_division_value_y = InputBox(
					50, HEIGHT-140, 140, 32, pg_font=self.fonts['inputbox'], plch=INP_DIV_Y_PLCH)

		self.input_phase = InputBox(
					270, HEIGHT-100, 0, 32, pg_font=self.fonts['inputbox'], plch=INP_PHASE_PLCH)
		self.input_ampl = InputBox(
					270, HEIGHT-140, 0, 32, pg_font=self.fonts['inputbox'], plch=INP_AMPL_PLCH)
		self.btn_set_sinusoid = Button(
					270, HEIGHT-60, 90, 32, pg_font=self.fonts['btn'], plch=BTN_SET_SIN_PLCH)

		
		self.btn_snapshoter = Button(
					480, HEIGHT-140, 74, 32, pg_font=self.fonts['btn'], plch=BTN_SNAP_PLCH)
		self.btn_add_overlay = Button(
					480, HEIGHT-60, 109, 32, pg_font=self.fonts['btn'], plch=BTN_ADD_OVERLAY_PLCH)
		self.btn_add_grid = Button(
					480, HEIGHT-100, 90, 32, pg_font=self.fonts['btn'], plch=BTN_ADD_GRID_PLCH)


	def __draw_inputboxes(self):
		self.input_function_box.draw(self.sc)
		self.input_division_value_x.draw(self.sc)
		self.input_division_value_y.draw(self.sc)

		self.input_phase.draw(self.sc)
		self.input_ampl.draw(self.sc)


	def __draw_btns(self):
		self.btn_snapshoter.draw(self.sc)
		self.btn_add_overlay.draw(self.sc)
		self.btn_add_grid.draw(self.sc)
		self.btn_set_sinusoid.draw(self.sc)


	def render_compns(self):
		self.__update_inputboxes()
		self.__draw_inputboxes()
		self.__draw_btns()
		self.field_controller.draw_axes(self.increasing_px_y, self.increasing_px_x)
		self.field_controller.draw_field()
		self.field_controller.draw_field_grid()


	def __update_inputboxes(self):
		self.input_function_box.update()
		self.input_division_value_x.update()
		self.input_division_value_y.update()

		self.input_phase.update()
		self.input_ampl.update()


	def handle_event(self, event):
		# Handles all events that may be associated with class components
		self.input_function_box.handle_event(event)
		self.input_division_value_x.handle_event(event)
		self.input_division_value_y.handle_event(event)

		self.input_phase.handle_event(event)
		self.input_ampl.handle_event(event)

		self.btn_snapshoter.handle_event(event)
		self.btn_set_sinusoid.handle_event(event)


	def get_func_polynomials(self)->FunctionRepr:
		# remove the placeholder "f(x)="
		func_body = self.input_function_box.text[len(INP_FUNC_PLCH):]
		if check_correct_func_polynom(func_body):
			func_polynomials = function_transform(func_body)
		else:
			func_polynomials = FunctionRepr(numerator=[], denominator=[])
		return func_polynomials


	def get_new_increasing(self, axic):
		try:
			if axic == 'x':
				new_increasing = int(self.input_division_value_x.text[len(INP_DIV_X_PLCH):])		
			elif axic == 'y':
				new_increasing =  int(self.input_division_value_y.text[len(INP_DIV_Y_PLCH):])	
		except ValueError as e:
			print('Uncorrect new increasing')
			return self.increasing_px_y if axic == 'y' else self.increasing_px_x
	
		if new_increasing > 0 and new_increasing <= 10:
			return new_increasing
		else:
			print("New increasing too much. Range for increasing: [0-10]")
			return self.increasing_px_y if axic == 'y' else self.increasing_px_x
	

	def get_sinusoid_phase(self)->int:
		new_phase = 1
		try:
			new_phase = int(self.input_phase.text[len(INP_PHASE_PLCH):])
		except ValueError as e:
			pass
		if new_phase == 0:
			print("phase kf mustn`t be equal to zero")
			return 1
		return new_phase

	def get_sinusoid_ampl(self)->int:
		new_ampl = 0
		try:
			new_ampl = int(self.input_ampl.text[len(INP_AMPL_PLCH):])
		except ValueError as e:
			pass
		return new_ampl


	def func_inp_is_active(self):
		return self.input_function_box.active

	def inp_div_x_is_active(self):
		return self.input_division_value_x.active

	def inp_div_y_is_active(self):
		return self.input_division_value_y.active

	def inp_phase_is_active(self):
		return self.input_phase.active

	def inp_ampl_is_active(self):
		return self.input_ampl.active


	def add_graphic_btn_is_active(self):
		return self.btn_add_overlay.blick