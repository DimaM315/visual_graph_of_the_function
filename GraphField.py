import pygame

from settings import * 


class GraphField:
	# Initial field and make math operation on field`s point

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
				pygame.draw.rect(self.sc, (0,0,0), (normal_x, normal_y, self.size_point, self.size_point))



	def is_point_of_field(self, x, y):
		# check point`s coords
		return (self.axes_boundaries['x_left'] < x < self.axes_boundaries['x_right'] and 
				self.axes_boundaries['y_top'] < y < self.axes_boundaries['y_bottom'])