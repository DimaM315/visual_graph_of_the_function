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


def draw_axes(sc, font_axes, font_axes_chair_v):
	antialias = 4
	serif_h = font_axes.render('|', antialias, RED)
	serif_v = font_axes_chair_v.render('_', antialias, RED)

	# draw serif
	for i in range(4):
		sc.blit(serif_h, (125 + i * DIVISION_VALUE_PX, HEITGHT_Y_AXIC_PX+TOP_PADDING_1))
		if i == 3: # dont make a vertical serif
			continue
		sc.blit(serif_v, (LEFT_PADDING_1, 235 - i * DIVISION_VALUE_PX))
	
	simbol_axic_name_y = font_axes.render('y', antialias, RED)
	sc.blit(simbol_axic_name_y, (LEFT_PADDING_1, TOP_PADDING_1))

	# axic x
	axic_x_values = get_axic_values(DIVISION_VALUE)
	for i, value in enumerate(axic_x_values):
		
		value_sprite = font_axes.render(value, antialias, RED)
		if value == '0':
			sc.blit(value_sprite, (LEFT_PADDING_1, HEITGHT_Y_AXIC_PX+TOP_PADDING_1+X_VALUES_TOP_PADDING))
			continue 
		sc.blit(value_sprite, (
					LEFT_PADDING_1 + i * DIVISION_VALUE_PX - 25, 
					HEITGHT_Y_AXIC_PX + TOP_PADDING_1 + X_VALUES_TOP_PADDING)
		)
	
	simbol_axic_name_x = font_axes.render('x', antialias, RED)
	sc.blit(simbol_axic_name_x, (
				WIDTH_X_AXIC_PX + LEFT_PADDING_1,
				HEITGHT_Y_AXIC_PX + TOP_PADDING_1)
	)
	

def function_transfor(func_str:str):
	# func_str kind of "x^3 + 4x^2 - 2x + 10"
	# return list will be [(a1, b1), (a2, b2)] a - coeff of polynomic, b - degree of x
	assert len(func_str) > 0 , "most short func_str is only x"

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

	print(func_parts)
		



if __name__ == '__main__':
	#print(get_axic_values(1000))
	function_transfor("-x^3 + 4x^2 - 2x - 10")