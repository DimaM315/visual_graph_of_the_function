from pympler import asizeof


from services.mathCore import MathCore


def report_mathCore():
	func_polynomials = [[(1, 1)],[]]
	inst = MathCore(func_polynomials=func_polynomials, mode='func')

	print('\n')
	print("### Start MathCore instance report ###")
	print("Size byte: " + str(asizeof.asized(inst).size))
	print("Refs on obj: " + str(asizeof.asized(inst).refs))
	print("-"*25)




if __name__ == '__main__':
	report_mathCore()