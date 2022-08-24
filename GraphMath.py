import math

from settings import WIDTH_X_AXIC_PX, DIVISION_VALUE, INCREASING_OF_PX

class GraphMath:
	"""Some math action for graphic of functions"""

	def __init__(self, start_x=0):
		self.mode = ''
		self.start_x = start_x
		self.last_x = INCREASING_OF_PX * WIDTH_X_AXIC_PX # for sequence compute
		self.activity_graph_function = None
	

	def function_seq(self, func_polynomials:list)->list:
		# the sequence is given by the function
		# shape of function have be: [(a,d1), (b,d2), (c,d3)] each tuple is just coeff of each polynomial and his deree. 
		# a - polinomial in zero deree, b - pol. in one deree etc. 
		seq_points = []
		
		for x in range(1, WIDTH_X_AXIC_PX):
			y = 0
			# "x" var should be as coords of x
			x_value = x * INCREASING_OF_PX 
			for pol_coeff, pol_degree in func_polynomials:
				y += pol_coeff * (x_value ** pol_degree)
			seq_points.append((x, y))

		return seq_points



	def sequence_gcd_counter(self)->list:
		# берем чисело из натуральной последовательности, и считаем сколько числе меньше него с 
		# наибольшим общим делителем равным 1
		# 1, 2, ... last_x
		seq = [1, 2]
		for n in range(3, self.last_x):
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
		for n in range(3, self.last_x):
			divisor_counter = 2
			for i in range(2, n//2+1):
				if n % i == 0:
					divisor_counter += 1
			seq.append(divisor_counter)
		return seq


	def conver_seq_to_point_list(self, seq:list)->list:
		# make the sequence point list, where x = number element of list, y = value element of list
		# :with_start_point - add (0;0) point or not
		point_list = []
		for i, value in enumerate(seq):
			x = i + 1 
			y = value
			point_list.append((x, y))
		return point_list


if __name__ == '__main__':
	m = GraphMath(400)
	print(m.function_seq([(2, 0)]))