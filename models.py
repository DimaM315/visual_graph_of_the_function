from typing import List, Tuple
import re

from settings import *
from entity_types import Polynom, FunctionRepr


def get_axic_values(division_value:int)->List[str]:
	# shape of value : n * 10^k , with the exception of zero
	assert type(division_value) == int, "division_value must be integer"
	if division_value < 100 or division_value > 1000:
		raise ValueError("division_value shouldn`t be so biggest")
	assert division_value % 100 == 0 , "division_value err, let's you enter a number a multiple of 100" 

	values_list = ["0"]

	degree_of_10 = 0
	while division_value >= 10:
		division_value = division_value / 10
		degree_of_10 += 1

	coeff = int(division_value)

	for i in range(1, 5):
		values_list.append("{0}*10^{1}".format(coeff * i, degree_of_10))

	return values_list


def function_transform(func_str:str)->FunctionRepr:
	# func_str kind of "x^3 + 4x^2 - 2x + 10"
	# return list will be [(a1, b1), (a2, b2)] a - coeff of polynomic, b - degree of x
	if len(func_str) == 0:
		raise ValueError("Short func_str in function_transform")

	func_str = func_str.lower().replace(' ', '').replace("(", "").replace(")", "")

	if "/" in func_str:
		polynomsNumerator = splitting_into_separete_polynimoals(func_str.split('/')[0])
		polynomsDenominator = splitting_into_separete_polynimoals(func_str.split('/')[1])
	else:
		polynomsNumerator = splitting_into_separete_polynimoals(func_str)
		polynomsDenominator = []

	return FunctionRepr(
			numerator=[str_poly_to_tuple_poly(poly) for poly in polynomsNumerator], 
			denominator=[str_poly_to_tuple_poly(poly) for poly in polynomsDenominator]
		)


def str_poly_to_tuple_poly(str_poly:str)->Polynom:
	# :strPoly - is one polynomial like k*x^d with type str.
	# return -> [k, d]
	"""
		strPolyToArrPoly("2x") --> [2, 1]
		strPolyToArrPoly("") --> raise Error
		strPolyToArrPoly("-8x^33") --> [-8, 33]
		strPolyToArrPoly("-8x^-33") --> [-8, -33]
	"""
	if str_poly == "": # unexpected value of str_poly
		raise ValueError("Empty str_poly in str_poly_to_tuple_poly")
	if str_poly == "x":
		return Polynom(kf=1.0, dg=1.0)
	if str_poly == "-x":
		return Polynom(kf=-1.0, dg=1.0)

	if "^" in str_poly: 
		# str_poly have shape: kx^d
		k = str_poly.split("x^")[0]
		d = str_poly.split("x^")[1]
		if k == "":
			k = "1"
		elif k == "-":
			k = "-1"
		return Polynom(kf=float(k), dg=float(d))
	elif "x" in str_poly: 
		# str_poly have shape: kx
		return Polynom(kf=float(str_poly.split("x")[0]), dg=1)
	else:
		# str_poly have shape: k
		return Polynom(kf=float(str_poly), dg=0) 

	
def splitting_into_separete_polynimoals(funcComponents:str)->List[str]:
	# Разбиваем числитель или знаменатель(funcComponents) на куски(Полиномы:str):list
	# :funcComponents - преведён к нормальному виду. Обрезаны все пробелы, символы с маленькой буквы и т.п.
	polynoms = []
	if funcComponents == "":
		raise ValueError("Empty funcComponents in splitting_into_separete_polynimoals")

	raw_store_polynoms = funcComponents.split("-") # funcComponents have shape: k1x^d1-k2x^d2+k3x^d3...

	if raw_store_polynoms[0] == "": # if funcComponents had started with "-"
		raw_store_polynoms[1] = "-" + raw_store_polynoms[1] # Then ceil in index 1 should start with "-"
		# delete empty ceil in index 0
		raw_store_polynoms = raw_store_polynoms[1:]

	if "^-" in funcComponents: # funcComponents had "^-" negotive degree.
		for i in range(len(raw_store_polynoms)):
			if raw_store_polynoms[i][-1] == "^":
				raw_store_polynoms[i] = raw_store_polynoms[i] + "-" + raw_store_polynoms[i+1]
				raw_store_polynoms.remove(raw_store_polynoms[i+1])
			if i == len(raw_store_polynoms)-1:
				break

	if len(raw_store_polynoms) == 1: # funcComponents had only one sing "-", just spliting by "+"
		if "+" in raw_store_polynoms[0]: # funcComponents had else "+" in himself.
			raw_store_polynoms = raw_store_polynoms[0].split("+")
		return raw_store_polynoms

	# funcComponents had more one sing "-"
	raw_store_polynoms = [raw_store_polynoms[0]] + ["-" + comp for comp in raw_store_polynoms[1:]]
	for comp in raw_store_polynoms:
		if "+" in comp:
			for poly in comp.split("+"):
				polynoms.append(poly) 
		else:
			polynoms.append(comp)

	return polynoms


def check_correct_func_polynom(func_body:str)->bool:
	if '/' in func_body:
		if func_body.endswith('/') or func_body.startswith('/'):
			return False
	return True





# TESTS
def test_function_transform():
	test1 = function_transform("-x^3 + 4x^2 - 2x - 10") == [[(-1, 3), (4, 2), (-2, 1), (-10, 0)], []]
	test2 = function_transform("x^5 - 6610") == [[(1.0, 5.0), (-6610.0, 0.0)], []]
	test3 = function_transform("-x^2") == [[(-1.0, 2.0)], []]
	test4 = function_transform("x^2") == [[(1.0, 2.0)], []]
	test5 = function_transform("-33x^3+1x") == [[(-33.0, 3.0), (1.0, 1.0)], []]
	test6 = function_transform("x+0") == [[(1.0, 1.0), (0, 0)], []]
	try:
		test7 = function_transform("+0-0") == [[], []]
	except ValueError as e:
		test7 = True
	else:
		test7 = False
	test8 = function_transform("1") ==[[(1.0, 0.0)], []]
	test9 = function_transform("x^0.5") ==[[(1.0, 0.5)], []]
	test10 = function_transform("0.5x^2") == [[(0.5, 2.0)], []]
	test11 = function_transform("0.33x^-11") == [[(0.33, -11)], []]

	# With bracket.
	test12 = function_transform("(x-3)/(x^2+3x)") == [[(1, 1), (-3, 0)], [(1, 2), (3, 1)]]
	test13 = function_transform("(2x^2 +x-3)/(x^2+3x)") == [[(2, 2), (1, 1), (-3, 0)], [(1, 2), (3, 1)]]

	test14 = function_transform("-x") == [[(-1, 1)],[]]

	results = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11,test12, test13, test14]
	print(str(results.count(True)) + "/" + str(len(results)))

	if False in results:
		print(results.index(False))


def test_get_y_by_x():
	# y = (x^2 - 10) / 2 
	# y(10)=45; y(5)=7.5; y(4)=3; y(1)=-4.5; y(100)=4995;
	func_polynomials1 = [
		[(1, 2), (-10, 0)], 
		[(2, 0)]
	]
	test1 = all([
			get_y_by_x(10, func_polynomials1) == 45,
			get_y_by_x(5, func_polynomials1) == 7.5,
			get_y_by_x(4, func_polynomials1) == 3,
			get_y_by_x(1, func_polynomials1) == -4.5,
			get_y_by_x(100, func_polynomials1) == 4995,
		])

	result = all([test1])
	print(result)


def test_str_poly_to_tuple_poly():
	test1 = str_poly_to_tuple_poly("2x") == (2, 1)
	
	try:
		str_poly_to_tuple_poly("")
	except ValueError as e:
		test2 = True
	
	test3 = str_poly_to_tuple_poly("-8x^33") == (-8, 33)
	test4 = str_poly_to_tuple_poly("-8x^-33") == (-8, -33)
	test5 = str_poly_to_tuple_poly("44") == (44, 0)
	test6 = str_poly_to_tuple_poly("x") == (1, 1)
	test7 = str_poly_to_tuple_poly("-1000") == (-1000, 0)
	test8 = str_poly_to_tuple_poly("-x^-1") == (-1, -1)

	result = [test1, test2, test3, test4, test5, test6, test7,test8]
	print(str(result.count(True)) + "/" + str(len(result)))


def test_splitting_into_separete_polynimoals():
	test1 = splitting_into_separete_polynimoals("2x") == ["2x"]
	
	try:
		splitting_into_separete_polynimoals("")
	except ValueError as e:
		test2 = True
	else:
		test2 = False
	
	test3 = splitting_into_separete_polynimoals("-8x^33+x^2-3x+10") == ["-8x^33", "x^2", "-3x", "10"]
	test4 = splitting_into_separete_polynimoals("-8x^-33") == ["-8x^-33"]

	test5 = splitting_into_separete_polynimoals("44") == ["44"]
	test6 = splitting_into_separete_polynimoals("x-10") == ["x", "-10"]
	test7 = splitting_into_separete_polynimoals("0x-1000") == ["0x", "-1000"]
	test8 = splitting_into_separete_polynimoals("3x+0x-5-x^-2-x^-3") == ["3x", "0x", "-5", "-x^-2", "-x^-3"]
	
	test9 = splitting_into_separete_polynimoals("-33x^3+x") == ["-33x^3", "x"]
	test10 = splitting_into_separete_polynimoals("-33x^-3+x") == ["-33x^-3", "x"]
	test11 = splitting_into_separete_polynimoals("-33x^-3-x") == ["-33x^-3", "-x"]


	result = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11]
	print(str(result.count(True)) + "/" + str(len(result)))


if __name__ == '__main__':
	test_splitting_into_separete_polynimoals()
	#test_function_transform()
	#test_str_poly_to_tuple_poly()
	#func = "(x^2+10+x^-1)/(x^3+10)"
	#func_poly = function_transform(func)
	#y_10 = get_y_by_x(10, poly)
	#print(y_10)