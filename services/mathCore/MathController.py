from loguru import logger
from typing import List, Tuple

from services.mathCore.Sequenses import Sequenses
from services.mathCore.Sinusoid import Sinusoid
from settings import WIDTH_X_AXIC_PX
from entity_types import GraphTypes, Coords, CanvasPoint, Polynom, FunctionRepr



logger.add("logs/error.log", format="{time} | {level} | {message}", level="ERROR", compression="zip", rotation="50 KB")

class MathCore:
	"""
		The mathCore component uses the concept of representing a given function 
		f(x) as a list of members(polynom) of the form (k,d). Each member of the functional 
		expression is k*(x^d).

		:func_polynomials - current function for graph. It have two list,
		first list is numerator, second is denominator. For calculate num_secuense 
		results these lists are multiple.
	"""

	def __init__(self, func:FunctionRepr=None, start_x:int=0, 
				mode:GraphTypes=GraphTypes.FUNC, sin_ampl:int=25, sin_phase_kf=32):
		# divisition value each px of field
		self.increasing_px_x = 5
		self.increasing_px_y = 5
		
		self.mode = mode
		self.start_x = start_x	

		self.__tmp_func = func
		self.tmp_sequence = 'increasing_decreasing_func'
		self.sinusoid_inst = Sinusoid(ampl=sin_ampl, phase_kf=sin_phase_kf)

		self.coords_list:List[Coords] = self.get_coords_list()


	def get_coords_list(self)->List[Coords]:
		if self.mode == GraphTypes.FUNC and self.__tmp_func is not None:
			coords_list = self.__get_coords_list_by_func()
		elif self.mode == GraphTypes.SEQUENCE:
			coords_list = self.__get_coords_list_by_seq()
		elif self.mode == GraphTypes.SINUSOID:
			coords_list = self.__get_coords_list_by_amplitude()
		else:
			logger.error("Undefind mode! Temporary mode is "+self.mode)
			return []
		return coords_list


	def set_tmp_func(self, new_func:FunctionRepr):
		if len(new_func) == 0 or len(new_func) > 2:
			logger.error("Given unexpected new_func in set_tmp_func")
		else:
			self.__tmp_func = new_func


	def set_sinusoid_params(self, phase_kf:int=None, new_ampl:int=None):
		if new_ampl != None:
			self.sinusoid_inst.set_ampl(new_ampl)
		if phase_kf != None:
			self.sinusoid_inst.set_phase(phase_kf)
			

	def __get_coords_list_by_func(self)->List[Coords]:
		# the sequence is given by the function
		# shape of function have be: [(a,d1), (b,d2), (c,d3)] each tuple is just coeff of each polynomial and his deree. 
		# a - polinomial in zero deree, b - pol. in one deree etc. 
		coords_list = []

		for x in range(1, WIDTH_X_AXIC_PX):
			# "x" var should be as coords of x
			y = int(self.__get_y_by_x(x*self.increasing_px_x, self.__tmp_func) / self.increasing_px_y)

			coords_list.append(Coords(x=x, y=y))
		return coords_list


	def __get_coords_list_by_seq(self)->List[Coords]:
		# make the sequence coords list, where x = number element of list, y = value element of list
		# :with_start_coords - add (0;0) coords or not

		# update the sequence
		coords_list = Sequenses.get_sequens_by_name(self.tmp_sequence, self.__get_last_x())
		return self.__coords_increasing(coords_list)

	
	def __get_coords_list_by_amplitude(self)->List[Coords]:
		coords_list = self.sinusoid_inst.get_coords_by(x0=0, x_last=self.__get_last_x())
		return self.__coords_increasing(coords_list)


	def __coords_increasing(self, coords_list:List[Coords])->List[Coords]:
		coords_increasing_list = []
		for coord in coords_list:
			if coord.x % self.increasing_px_x == 0:
				x = coord.x // self.increasing_px_x
				y = coord.y // self.increasing_px_y
				coords_increasing_list.append(Coords(x=x, y=y))
		return coords_increasing_list


	def __get_y_by_x(self, x:int, func:FunctionRepr)->float:
		y_numerator = sum([kf*(x**dg) for kf, dg in func.numerator])
		y_denominator = sum([kf*(x**dg) for kf, dg in func.denominator])

		if len(func.denominator) == 0:
			# Denominator dont exist
			return y_numerator
		elif y_denominator == 0:
			# Denominator is exist and equal 0. In the case y=infinite
			return 10**6

		# Always round up to the 2nd digit before dot
		y = int((y_numerator/y_denominator)*100)/100
		return y


	def __get_last_x(self)->int:
		return self.increasing_px_x * WIDTH_X_AXIC_PX

		



# TESTS
def test_empty_MathCore():
	m = MathCore()
	last_x = m.get_last_x()

	test1 = m.tmp_func == None and m.sequence == None and m.start_x == 0
	test2 = m.get_coords_list_by_func() == None
	test3 = m.get_coords_list() == None

	result = all([test1, test2, test3])
	print(result)


def test_change_mode_MathCore():
	m = MathCore([(1, 1), (2, 0.5), (24, 0)])

	test1 = isinstance(m.tmp_func, list) and m.sequence == None and m.mode == 'func' and m.get_coords_list_by_seq() == None
	
	m.mode = 'seq'
	m.increasing_px_x = 1
	test_sequence = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6)]
	m.sequence = test_sequence
	m.tmp_sequence = "none"
	coords_list_by_seq = m.get_coords_list_by_seq()

	test2 = m.get_coords_list_by_func() == None and isinstance(coords_list_by_seq, list) and len(test_sequence) == len(coords_list_by_seq)

	test3 = m.get_coords_list() == coords_list_by_seq

	m.mode = 'func'
	coords_list = m.get_coords_list()
	test4 = True
	for i in range(len(coords_list)-1):
		if coords_list[i][0] != i + 1:
			test4 = False

	result = all([test1, test2, test3, test4])
	print(result)


if __name__ == '__main__':
	test_empty_MathCore()
	test_change_mode_MathCore()
	
	func = [
		[(2,2), (3,0)],
		[]
	]

	m = MathCore(func)
	print(m.mode, m.func)
	#print(m.get_coords_list())