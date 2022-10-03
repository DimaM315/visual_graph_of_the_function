import time


from MathCore import MathCore
from models import get_axic_values

def test_empty_MathCore():
	m = MathCore()
	last_x = m.get_last_x()

	test1 = m.func_polynomials == None and m.sequence == None and m.start_x == 0
	test2 = m.function_handler() == None
	test3 = m.get_point_list() == None

	result = all([test1, test2, test3])
	print('Result of test_empty_MathCore is : ', result)


def test_change_mode_MathCore():
	m = MathCore([(1, 1), (2, 0.5), (24, 0)])

	test1 = isinstance(m.func_polynomials, list) and m.sequence == None and m.mode == 'func' and m.get_point_list_by_seq() == None
	
	m.mode = 'seq'
	test_sequence = [1,2,3,4,5,6]
	m.sequence = test_sequence
	point_list_by_seq = m.get_point_list_by_seq()

	test2 = m.function_handler() == None and isinstance(point_list_by_seq, list) and len(test_sequence) == len(point_list_by_seq)
	test3 = m.get_point_list() == point_list_by_seq

	result = all([test1, test2, test3])
	print('Result of test_change_mode_MathCore is : ', result)



def test_models_get_axic_values():
	axic_values_1 = get_axic_values(100)
	test1 = axic_values_1[0] == '0' and axic_values_1[1] == '1*10^2' and len(axic_values_1) == 5

	axic_values_2 = get_axic_values(1000)
	test2 = axic_values_2[0] == '0' and axic_values_2[1] == '1*10^3' and len(axic_values_2) == 5

	axic_values_3 = get_axic_values(300)
	test3 = axic_values_3[0] == '0' and axic_values_3[1] == '3*10^2' and len(axic_values_3) == 5


	test4 = False
	try:
		axic_values_4 = get_axic_values(0)
	except ValueError as e:
		test4 = True

	test5 = False
	try:
		axic_values_5 = get_axic_values(120000)
	except ValueError as e:
		test5 = True

	result = all([test1, test2, test3, test4, test5])
	print('Result of test_models_get_axic_values is : ', result)



def test_get_point_list():
	m = MathCore()
	m.func_polynomials = [(1, 0.5)] # squere root

	start_time = time.time()
	m.get_point_list()
	print('the function get_point_list have been worked for {0} seconds'.format(str(time.time()-start_time)[:5]))


	m.func_polynomials = [(1, 32), (13, 234), (28, 0.53), (11, 355.5), (17, 14.5)] # hard function
	m.increasing_px_x = 10 # max increasing
	start_time = time.time()
	point_list_1 = m.get_point_list()
	print('the function get_point_list have been worked for {0} seconds'.format(str(time.time()-start_time)[:5]))


	m.increasing_px_x = 1
	point_list_2 = m.get_point_list()
	test1 = len(point_list_1) == len(point_list_2)

	result = all([test1])
	print('Result of test_get_point_list is : ', result)


if __name__ == '__main__':
	#test_empty_MathCore()
	#test_change_mode_MathCore()
	#test_models_get_axic_values()
	test_get_point_list()