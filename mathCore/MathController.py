from mathCore.Sequenses import Sequenses

from models import get_y_by_x
from settings import WIDTH_X_AXIC_PX


class MathCore:
	"""
		Some math action for graphic of functions.
		When the mode is "seq" don`t allow to change increasing_px

		:func_polynomials - current function for graph. It have two list,
		first list is numerator, second is denominator. For calculate num_secuense 
		results these lists are multiple.
	"""

	def __init__(self, func_polynomials=None, start_x=0, mode='func'):
		# divisition value each px of field
		self.increasing_px_x = 5
		self.increasing_px_y = 5
		
		self.mode = mode
		self.start_x = start_x	

		#  with shape: [ [(k1, d1), (10, 0)], [((k1, d1), (10, 0))] ]
		self.func_polynomials = func_polynomials
	
		# current sequence of number with shape [n1, n2, n3]
		self.sequence = Sequenses.sequence_rand_numbers(self.get_last_x()) if mode == 'seq' else None
		self.tmp_sequence = 'sequence_rand_numbers'
		self.point_list = None


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
			# "x" var should be as coords of x
			y = int(get_y_by_x(x*self.increasing_px_x, self.func_polynomials) / self.increasing_px_y)

			seq_points.append((x, y))
		return seq_points


	def get_point_list_by_seq(self)->list:
		# make the sequence point list, where x = number element of list, y = value element of list
		# :with_start_point - add (0;0) point or not
		if self.mode != 'seq' or self.sequence is None:
			return None

		# update the sequence
		self.sequence = Sequenses.get_sequens_by_name(self.tmp_sequence, self.get_last_x())

		point_list = []
		for i, value in enumerate(self.sequence):
			if i % self.increasing_px_x == 0:
				x = i // self.increasing_px_x
				y = value[1] // self.increasing_px_y
				point_list.append((x, y))
		return point_list

		



# TESTS
def test_empty_MathCore():
	m = MathCore()
	last_x = m.get_last_x()

	test1 = m.func_polynomials == None and m.sequence == None and m.start_x == 0
	test2 = m.function_handler() == None
	test3 = m.get_point_list() == None

	result = all([test1, test2, test3])
	print(result)


def test_change_mode_MathCore():
	m = MathCore([(1, 1), (2, 0.5), (24, 0)])

	test1 = isinstance(m.func_polynomials, list) and m.sequence == None and m.mode == 'func' and m.get_point_list_by_seq() == None
	
	m.mode = 'seq'
	m.increasing_px_x = 1
	test_sequence = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6)]
	m.sequence = test_sequence
	m.tmp_sequence = "none"
	point_list_by_seq = m.get_point_list_by_seq()

	test2 = m.function_handler() == None and isinstance(point_list_by_seq, list) and len(test_sequence) == len(point_list_by_seq)

	test3 = m.get_point_list() == point_list_by_seq

	m.mode = 'func'
	point_list = m.get_point_list()
	test4 = True
	for i in range(len(point_list)-1):
		if point_list[i][0] != i + 1:
			test4 = False

	result = all([test1, test2, test3, test4])
	print(result)


if __name__ == '__main__':
	#test_empty_MathCore()
	#test_change_mode_MathCore()
	
	func_polynomials = [
		[(2,2), (3,0)],
		[]
	]

	m = MathCore(func_polynomials)
	print(m.mode, m.func_polynomials)
	#print(m.get_point_list())