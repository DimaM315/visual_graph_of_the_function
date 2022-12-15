import math
from typing import List

from entity_types import Coords


class Sinusoid:

	def __init__(self, ampl:int=1, phase_kf:int=16):
		self.__phase = math.pi / phase_kf
		self.__ampl = ampl
		self.type = 'sin'


	def get_coords_by(self, x0:int, x_last:int)->List[Coords]:
		coords = []
		offset = self.__ampl + 5
		
		for x in range(x0, x_last):
			y = self.__ampl * math.sin(self.__phase * x)
			coords.append(Coords(x=x, y=int(y + offset)))
		
		return coords

	def set_ampl(self, new_ampl:int):
		self.__ampl = new_ampl

	def set_phase(self, phase_kf:int):
		self.__phase = math.pi / phase_kf
 




if __name__ == '__main__':
	amp_inst = Sinusoid()
	amp_inst.get_coords_by(0, 15)



