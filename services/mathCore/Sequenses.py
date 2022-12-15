import math
import random
from typing import List

from entity_types import Coords


class Sequenses:
	@staticmethod
	def get_sequens_by_name(seq_name:str, last_x:int)->List[Coords]:
		# :last_x - последний элемент послед-сти. Говорит о том сколько элементов будет в исходном списке.
		point_list = []
		if seq_name == 'gcd_counter':
			point_list = Sequenses.sequence_gcd_counter(last_x)
		elif seq_name == 'sequence_divisor_counter':
			point_list = Sequenses.sequence_divisor_counter(last_x)
		elif seq_name == 'sequence_test':
			point_list = Sequenses.sequence_test(last_x)
		elif seq_name == 'increasing_decreasing_func':
			point_list = Sequenses.increasing_decreasing_func(last_x)
		elif seq_name == "sequence_rand_numbers":
			point_list = Sequenses.sequence_rand_numbers(last_x)
		return point_list


	@staticmethod
	def sequence_gcd_counter(last_x:int)->List[Coords]:
		# берем чисело из натуральной послед-сти, и считаем сколько числе меньше него с 
		# наибольшим общим делителем равным 1
		# 1, 2, ... last_x
		seq = [Coords(x=1, y=1), Coords(x=2, y=2)]
		for n in range(3, last_x):
			gcd_counter = 1
			for i in range(1, n):
				if math.gcd(i, n) == 1:
					gcd_counter += 1
			seq.append(Coords(x=n, y=gcd_counter))
		return seq


	@staticmethod
	def sequence_divisor_counter(last_x:int)->List[Coords]:
		# Последовательность из кол-ва делителей натуральных чисел.
		# 1, 2, ... WIDTH_X_AXIC_PX
		seq = [Coords(x=1, y=1), Coords(x=2, y=2)]
		for n in range(3, last_x):
			divisor_counter = 2
			for i in range(2, n//2+1):
				if n % i == 0:
					divisor_counter += 1
			seq.append(Coords(x=n, y=divisor_counter))
		return seq


	@staticmethod
	def sequence_rand_numbers(last_x:int)->List[Coords]:
		seq = []
		for n in range(1, last_x):
			seq.append(Coords(x=n, y=random.randint(0, last_x)))
		return seq


	@staticmethod
	def increasing_decreasing_func(last_x:int)->List[Coords]:
		seq = []
		for x in range(1, last_x):
			numerator = 2*((x + 1)**2) + 0.5*((x-32)**3)
			denominator =  (x - 22)
			if denominator != 0:
				y = numerator / denominator
			seq.append(Coords(x=x, y=y))
		return seq


	@staticmethod
	def sequence_test(last_x:int)->List[Coords]:
		# y = 9 * (x/3 + 10)
		seq = []
		for x in range(1, last_x):
			y = 9*(x/100 + 10) 
			seq.append(Coords(x=x, y=int(y)))
		return seq 



if __name__ == '__main__':
	print(Sequenses.get_sequens_by_name("sequence_divisor_counter", 10))