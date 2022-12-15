import math
from typing import List

from entity_types import Coords, FunctionRepr


class Func:
	def __init__(self, func:FunctionRepr=None):
		self.numerator = func.numerator
		self.denominator = func.denominator
		

	def get_coords_by(self, x0:int, x_last:int)->List[Coords]:
		coords = []
		for x in range(x0, x_last):
			y = self.get_y_by_x(x)
			coords.append(Coords(x=x, y=y))
		return coords


	def set_funcRepr(self, new_func:FunctionRepr):
		self.numerator = new_func.numerator
		self.denominator = new_func.denominator


	def get_y_by_x(self, x:int)->int:
		y_numerator = sum([kf*(x**dg) for kf, dg in self.numerator])
		y_denominator = sum([kf*(x**dg) for kf, dg in self.denominator])

		if len(self.denominator) == 0:
			# Denominator dont exist
			return y_numerator
		elif y_denominator == 0:
			# Denominator is exist and equal 0. In the case y=infinite
			return 10**6

		# Always round up to the 2nd digit before dot
		y = int((y_numerator/y_denominator)*100)/100
		return y