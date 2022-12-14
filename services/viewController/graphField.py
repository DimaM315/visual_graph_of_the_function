import pygame
from typing import List

from settings import *
from models import get_axic_values
from entity_types import CanvasPoint, Coords



class GraphFieldController:
	# Initialize field and vizualize math operation on field`s point

	def __init__(self, screen, fonts_axes, fonts_axes_chair_y):
		# field`s start point(0;0) in pg`s coords
		self.zero_point = CanvasPoint(x=LEFT_PADDING_2 + LEFT_PADDING_1, y=HEITGHT_Y_AXIC_PX + TOP_PADDING_1-1) 
		self.size_point = 2

		self.sc = screen

		self.fonts_axes = fonts_axes
		self.fonts_axes_chair_y = fonts_axes_chair_y
		self.__grid_active = False


	def draw_field(self):	
		pygame.draw.rect(self.sc, WHITE, (LEFT_PADDING_1 + LEFT_PADDING_2, TOP_PADDING_1, WIDTH_X_AXIC_PX, HEITGHT_Y_AXIC_PX))


	def draw_field_grid(self):
		if self.__grid_active:
			for i in (1,2,3):
				pygame.draw.rect(self.sc, BLUE, (
					self.zero_point.x, self.zero_point.y-i*100, WIDTH_X_AXIC_PX, 1))
				pygame.draw.rect(self.sc, BLUE, (
					self.zero_point.x+i*100, self.zero_point.y-HEITGHT_Y_AXIC_PX, 1, HEITGHT_Y_AXIC_PX))
			pygame.draw.rect(self.sc, BLUE, (
					self.zero_point.x+400, self.zero_point.y-HEITGHT_Y_AXIC_PX, 1, HEITGHT_Y_AXIC_PX))


	def toggle_field_grid(self):
		self.__grid_active = not self.__grid_active


	def draw_coords_list(self, coords_list:List[Coords]):
		# drawing computed massive of math coords

		for x, y in coords_list:	
			normal_x = self.zero_point.x + x
			normal_y = self.zero_point.y - y
			if normal_y > 0:
				pygame.draw.rect(self.sc, BLACK, (normal_x, normal_y, self.size_point, self.size_point))


	def draw_axes(self, increasing_px_y:int, increasing_px_x:int):
		antialias = 4
		serif_x = self.fonts_axes.render('|', antialias, RED)
		serif_y = self.fonts_axes_chair_y.render('_', antialias, RED)

		self.__draw_serif(serif_x, serif_y)
		self.__draw_axic('x', increasing_px_x, increasing_px_y)
		self.__draw_axic('y', increasing_px_x, increasing_px_y)


	def __draw_axic(self, axic_name:str, increasing_px_x:int, increasing_px_y:int, antialias=4):
		padding_zero_char = (LEFT_PADDING_1, HEITGHT_Y_AXIC_PX+TOP_PADDING_1+X_VALUES_TOP_PADDING)
		
		if axic_name == 'y':
			padding_simbol_char = (LEFT_PADDING_1, TOP_PADDING_1)
			division_value = increasing_px_y * DIVISION_VALUE_PX	
		elif axic_name == 'x':
			padding_simbol_char = (WIDTH_X_AXIC_PX + LEFT_PADDING_1, HEITGHT_Y_AXIC_PX + TOP_PADDING_1)
			division_value = increasing_px_x * DIVISION_VALUE_PX

		axic_values = get_axic_values(division_value)
		
		for i, value in  enumerate(axic_values):
			value_sprite = self.fonts_axes.render(value, antialias, RED)
			if value == '0':
				self.sc.blit(value_sprite, (padding_zero_char))
				continue
			if axic_name == 'y':
				padding_for_each_value = (
						0, HEITGHT_Y_AXIC_PX+TOP_PADDING_1- i*DIVISION_VALUE_PX)	
			elif axic_name == 'x':
				padding_for_each_value = (
						LEFT_PADDING_1 + i * DIVISION_VALUE_PX - 25, 
						HEITGHT_Y_AXIC_PX + TOP_PADDING_1 + X_VALUES_TOP_PADDING)

			self.sc.blit(value_sprite, (padding_for_each_value[0], padding_for_each_value[1]))

		simbol_axic_name = self.fonts_axes.render(axic_name, antialias, RED)
		self.sc.blit(simbol_axic_name, (padding_simbol_char))	


	def __draw_serif(self, serif_x, serif_y):
		for i in range(4):
			self.sc.blit(serif_x, (self.zero_point.x + (i+1) * DIVISION_VALUE_PX-3, self.zero_point.y))
			if i == 3: # dont make 4th a serif x
				continue
			self.sc.blit(serif_y, (LEFT_PADDING_1, 240 - i * DIVISION_VALUE_PX+3))
