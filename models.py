from settings import *


def get_axic_values(division_value_px):
	# shape of value : n * 10^k , with the exception of zero
	assert type(division_value_px) == int, "division_value_px must be integer"
	assert division_value_px >= 100 and division_value_px <= 1000, "division_value_px shouldn`t be so biggest"
	assert division_value_px % 100 == 0 , "division_value_px err, let's you enter a number a multiple of 100" 

	values_list = ["0"]

	degree_of_10 = 0
	while division_value_px >= 10:
		division_value_px = division_value_px / 10
		degree_of_10 += 1

	coeff = int(division_value_px)

	for i in range(1, 5):
		values_list.append("{0}*10^{1}".format(coeff * i, degree_of_10))

	return values_list


def function_transform(func_str:str):
	# func_str kind of "x^3 + 4x^2 - 2x + 10"
	# return list will be [(a1, b1), (a2, b2)] a - coeff of polynomic, b - degree of x
	if len(func_str) == 0:
		raise ValueError("most short func_str is x")

	func_str = func_str.lower().replace(' ', '')
	polynomic_list = []

	# split by parts
	func_parts = []
	tmp_parts = ''
	for s in func_str:
		if s in ['+', '-']:
			if len(tmp_parts): 
				func_parts.append(tmp_parts)
			tmp_parts = ''
		tmp_parts += s
	else:
		func_parts.append(tmp_parts)

	for part in func_parts:
		if 'x' not in part:
			if part == '0' or part == '+0' or part == '-0':
				continue
			k, d = int(part), 0
		elif 'x' in part and '^' not in part:
			# just '-kx' one degree
			k, d = part.replace('x', ''), 1
		elif 'x' in part and '^' in part:
			# -kx^d
			k, d = part.split('x^')
		else:
			# with the correct shape of the function, the program will not reach this place
			raise ValueError('Uncorrect function shape')

		if k == '-':
			k = '-1'
		elif k == '+' or k == '':
			k = '1'
		polynomic_list.append((float(k), float(d)))

	return polynomic_list


def allowed_chars(event_unicode:str)->str:
	# restrict the user in the ability to use other characters except:
	# x 0-9 ^ + - .
	allowed_chars_list = ['x', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '^', '+', '-', '.']
	if event_unicode not in allowed_chars_list:
		print("we dont type any char except: 0-9 x + - ^ .")
		return ''
	return event_unicode


if __name__ == '__main__':
	print(get_axic_values(1000))
	function_transform("-x^3 + 4x^2 - 2x - 10")
	function_transform("+x^5 - 6610")
	function_transform("-x^2")
	function_transform("+x^2")
	function_transform("-33x^3+1x+0")
	function_transform("x+0")
	function_transform("+0-0")
	function_transform("1")
	function_transform("x^0.5")
	print(function_transform("0.5x^2"))
	
