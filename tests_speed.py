import time
import sys
from loguru import logger 



logger.add("logs/speed.log", format="{time} | {message}", level="INFO", compression="zip", rotation="50 KB")


if sys.version_info.minor == 11:
	# python3.11
	sys.path.append("C:\\Users\\User\\Desktop\\python\\project\\graph_func")

from models import function_transform

def test_func_transform():
	expression = ""
	count_poly = 1960
	count_iterations = 10
	py_version = "3."+str(sys.version_info.minor)
	
	for i in range(count_poly, 0, -1):
		expression += f"-{i+10}x^{i}"
	#print("exp: "+expression)
	
	time_after = time.time()
	for i in range(count_iterations):
		function_transform(f"({expression}+10)/({expression}-13)")
	time_overall = time.time() - time_after
	
	func_name = "function_transform(): "
	msg = f"time_overall={time_overall} | count_poly={count_poly} | count_iterations={count_iterations} | py_version={py_version}"
	
	logger.info(func_name+msg)
	


if __name__ == "__main__":
	test_func_transform()