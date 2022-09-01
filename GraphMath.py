import math

from settings import WIDTH_X_AXIC_PX

class GraphMath:
	"""Some math action for graphic of functions"""

	def __init__(self, func_polynomials=None, sequence=None, start_x=0, mode='func'):
		# divisition value each px of field
		self.increasing_px_x = 1
		self.increasing_px_y = 1
		
		self.mode = mode
		self.start_x = start_x		

		# current function on graph with shape: [(k1, d1), (10, 0)]
		self.func_polynomials = func_polynomials
		# current sequence of number with shape [n1, n2, n3]
		self.sequence = sequence


	def get_last_x(self)->int:
		return self.increasing_px_x * WIDTH_X_AXIC_PX


	def get_point_list(self)->list:
		point_list = None
		if self.mode == 'func' and self.func_polynomials is not None:
			point_list = self.function_handler()
		elif self.mode == 'seq' and self.sequence is not None:
			point_list = self.get_point_list_by_seq()
		else:
			print('Maybe you forgot change mode in GraphMath')
		return point_list


	def function_handler(self)->list:
		# the sequence is given by the function
		# shape of function have be: [(a,d1), (b,d2), (c,d3)] each tuple is just coeff of each polynomial and his deree. 
		# a - polinomial in zero deree, b - pol. in one deree etc. 
		seq_points = []
		
		if self.mode != 'func' or self.func_polynomials is None:
			return None

		for x in range(1, WIDTH_X_AXIC_PX):
			y = 0
			# "x" var should be as coords of x
			x_value = x * self.increasing_px_x 

			for pol_coeff, pol_degree in self.func_polynomials:
				y += pol_coeff * (x_value ** pol_degree)
				y = y // self.increasing_px_y
			seq_points.append((x, y))

		return seq_points


	def sequence_gcd_counter(self)->list:
		# берем чисело из натуральной последовательности, и считаем сколько числе меньше него с 
		# наибольшим общим делителем равным 1
		# 1, 2, ... last_x
		seq = [1, 2]
		for n in range(3, self.get_last_x()):
			gcd_counter = 1
			for i in range(1, n):
				if math.gcd(i, n) == 1:
					gcd_counter += 1
			seq.append(gcd_counter)
		return seq


	def sequence_divisor_counter(self)->list:
		# последовательность из кол-ва делителей чисел из натуральной последовательности
		# 1, 2, ... WIDTH_X_AXIC_PX
		seq = [1, 2]
		for n in range(3, self.get_last_x()):
			divisor_counter = 2
			for i in range(2, n//2+1):
				if n % i == 0:
					divisor_counter += 1
			seq.append(divisor_counter)
		return seq


	def get_point_list_by_seq(self)->list:
		# make the sequence point list, where x = number element of list, y = value element of list
		# :with_start_point - add (0;0) point or not
		if self.mode != 'seq' or self.sequence is None:
			return None

		point_list = []
		for i, value in enumerate(self.sequence):
			x = i + 1 
			y = value
			point_list.append((x, y))
		return point_list


	def __setattr__(self, attrname, value):
		if attrname == 'increasing_px_x' and self.__dict__.get('mode', 1) == 'seq':
			if self.increasing_px_x != value:
				print('increasing_px_x has been changed, please update the sequence')
		elif attrname == 'increasing_px_y' and self.__dict__.get('mode', 1) == 'seq':
			if self.increasing_px_y != value:
				print('increasing_px_y has been changed, please update the sequence')
		self.__dict__[attrname] = value


# TESTS
def test_empty_GraphMath():
	m = GraphMath()
	last_x = m.get_last_x()

	test1 = m.func_polynomials == None and m.sequence == None and m.start_x == 0
	test2 = m.function_handler() == None
	test3 = m.get_point_list() == None

	result = all([test1, test2, test3])
	print(result)


def test_change_mode_GraphMath():
	m = GraphMath([(1, 1), (2, 0.5), (24, 0)])

	test1 = isinstance(m.func_polynomials, list) and m.sequence == None and m.mode == 'func' and m.get_point_list_by_seq() == None
	
	m.mode = 'seq'
	test_sequence = [1,2,3,4,5,6]
	m.sequence = test_sequence
	point_list_by_seq = m.get_point_list_by_seq()

	test2 = m.function_handler() == None and isinstance(point_list_by_seq, list) and len(test_sequence) == len(point_list_by_seq)
	test3 = m.get_point_list() == point_list_by_seq

	result = all([test1, test2, test3])
	print(result)


if __name__ == '__main__':
	#test_empty_GraphMath()
	test_change_mode_GraphMath()