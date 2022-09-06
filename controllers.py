import pygame

from settings import *
from models import get_axic_values, function_transform, allowed_chars


class GraphFieldController:
	# Initialize field and vizualize math operation on field`s point

	def __init__(self, screen):
		# field`s start point(0;0) in pg`s coords
		self.zero_point_coords = (LEFT_PADDING_2+LEFT_PADDING_1, HEITGHT_Y_AXIC_PX+TOP_PADDING_1-1) 
		self.size_point = 1

		# field boundaries in pg`s coords
		self.axes_boundaries = {
					'x_left': LEFT_PADDING_2, 'x_right':LEFT_PADDING_2+WIDTH_X_AXIC_PX,
					'y_top': TOP_PADDING_1, 'y_bottom': TOP_PADDING_1+HEITGHT_Y_AXIC_PX}

		self.sc = screen


	def draw_field(self):	
		pygame.draw.rect(self.sc, WHITE, (LEFT_PADDING_1 + LEFT_PADDING_2, TOP_PADDING_1, WIDTH_X_AXIC_PX, HEITGHT_Y_AXIC_PX))


	def draw_points_list(self, points_list:list):
		# drawing computed massive of math point
		for x, y in points_list:
			normal_x = self.zero_point_coords[0] + x
			normal_y = self.zero_point_coords[1] - y
			if self.is_point_of_field(normal_x, normal_y):
				pygame.draw.rect(self.sc, BLACK, (normal_x, normal_y, self.size_point, self.size_point))



	def is_point_of_field(self, x, y):
		# check point`s coords
		return (self.axes_boundaries['x_left'] < x < self.axes_boundaries['x_right'] and 
				self.axes_boundaries['y_top'] < y < self.axes_boundaries['y_bottom'])


class CompnsController:
	# Initialize and maintain other components: axic, inputboxes, text.
	# In other words, the class controls any entity except for the field

	def __init__(self, screen, fonts:dict, increasing_px_x:int, increasing_px_y:int):
		# :fonts - dict of necessary fonts for initialize some components
		self.sc = screen
		self.fonts = fonts

		
		self.increasing_px_x = increasing_px_x
		self.increasing_px_y = increasing_px_y

		self.field_controller = GraphFieldController(self.sc)

		self.input_function_box = InputBox(
					100, HEIGHT-60, 140, 32, pg_font=self.fonts['inputbox'], plch=INP_FUNC_PLCH)
		self.input_division_value_x = InputBox(
					100, HEIGHT-100, 140, 32, pg_font=self.fonts['inputbox'], plch=INP_DIV_X_PLCH)
		self.input_division_value_y = InputBox(
					100, HEIGHT-140, 140, 32, pg_font=self.fonts['inputbox'], plch=INP_DIV_Y_PLCH)


	def draw_axes(self):
		antialias = 4
		serif_x = self.fonts['axes'].render('|', antialias, RED)
		serif_y = self.fonts['axes_chair_y'].render('_', antialias, RED)

		# draw serif
		for i in range(4):
			self.sc.blit(serif_x, (125 + i * DIVISION_VALUE_PX, HEITGHT_Y_AXIC_PX+TOP_PADDING_1))
			if i == 3: # dont make 4th a serif x
				continue
			self.sc.blit(serif_y, (LEFT_PADDING_1, 240 - i * DIVISION_VALUE_PX))
		
		self.draw_axic('x', antialias)
		self.draw_axic('y', antialias)


	def draw_axic(self, axic_name, antialias=4):
		padding_zero_char = (LEFT_PADDING_1, HEITGHT_Y_AXIC_PX+TOP_PADDING_1+X_VALUES_TOP_PADDING)	
		
		if axic_name == 'y':
			padding_simbol_char = (LEFT_PADDING_1, TOP_PADDING_1)
			division_value = self.increasing_px_y * DIVISION_VALUE_PX	
		elif axic_name == 'x':
			padding_simbol_char = (WIDTH_X_AXIC_PX + LEFT_PADDING_1, HEITGHT_Y_AXIC_PX + TOP_PADDING_1)
			division_value = self.increasing_px_x * DIVISION_VALUE_PX

		axic_values = get_axic_values(division_value)
		
		for i, value in  enumerate(axic_values):
			value_sprite = self.fonts['axes'].render(value, antialias, RED)
			if value == '0':
				self.sc.blit(value_sprite, (padding_zero_char))
				continue
			if axic_name == 'y':
				padding_for_each_value = (
						LEFT_PADDING_1-40, 
						HEITGHT_Y_AXIC_PX+TOP_PADDING_1-5- i*DIVISION_VALUE_PX)	
			elif axic_name == 'x':
				padding_for_each_value = (
						LEFT_PADDING_1 + i * DIVISION_VALUE_PX - 25, 
						HEITGHT_Y_AXIC_PX + TOP_PADDING_1 + X_VALUES_TOP_PADDING)

			self.sc.blit(value_sprite, (padding_for_each_value[0], padding_for_each_value[1]))

		simbol_axic_name = self.fonts['axes'].render(axic_name, antialias, RED)
		self.sc.blit(simbol_axic_name, (padding_simbol_char))	


	def draw_inputboxes(self):
		self.input_function_box.draw(self.sc)
		self.input_division_value_x.draw(self.sc)
		self.input_division_value_y.draw(self.sc)


	def render_compns(self):
		self.update_inputboxes()
		self.draw_inputboxes()

		self.draw_axes()
		self.field_controller.draw_field()


	def update_inputboxes(self):
		self.input_function_box.update()
		self.input_division_value_x.update()
		self.input_division_value_y.update()


	def handle_event(self, event):
		# Handles all events that may be associated with class components
		self.input_function_box.handle_event(event)
		self.input_division_value_x.handle_event(event)
		self.input_division_value_y.handle_event(event)


	def get_func_polynomials(self):
		# remove the placeholder "f(x)="
		func_body = self.input_function_box.text[len(INP_FUNC_PLCH):]
		func_polynomials = function_transform(func_body)
		return func_polynomials


	def get_new_increasing(self, axic):
		try:
			if axic == 'x':
				return int(self.input_division_value_x.text[len(INP_DIV_X_PLCH):])
			elif axic == 'y':
				return int(self.input_division_value_y.text[len(INP_DIV_Y_PLCH):])
		except ValueError as e:
			print('Uncorrect new increasing')
			return self.increasing_px_y if axic == 'y' else self.increasing_px_x
		

	def func_inp_is_active(self):
		return self.input_function_box.active

	def inp_div_x_is_active(self):
		return self.input_division_value_x.active

	def inp_div_y_is_active(self):
		return self.input_division_value_y.active


class InputBox:
    # Accepts the characters for input when pressing Enter
	# processes the entered value. Deletes the previously entered values
	# when pressing backspace, but doesn`t touch the placeholder

    def __init__(self, x, y, w, h, pg_font, plch):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = plch
        
        self.plch = plch
        
        self.pg_font = pg_font
        self.txt_surface = self.pg_font.render(self.text, True, self.color)
        self.active = False

        # Maximum number of characters for self.text
        self.limited_chars = 16 


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box
            self.color = GREEN if self.active else GRAY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print('Entered: ' + self.text)
                    self.text = self.plch
                    self.active = False
                    self.color = GREEN if self.active else GRAY
                elif event.key == pygame.K_BACKSPACE and len(self.text) > len(self.plch):
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <  self.limited_chars:
                        self.text += allowed_chars(event.unicode)
                # Re-render the text
                self.txt_surface = self.pg_font.render(self.text, True, self.color)


    def update(self):
        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width


    def draw(self, screen):
        # Blit the text and the rect 
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)