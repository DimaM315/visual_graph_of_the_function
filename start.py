from loguru import logger

from services import MathCore
from main import app



logger.add("logs/error.log", format="{time} | {level} | {message}", level="ERROR", compression="zip", rotation="50 KB")

@logger.catch
def start():
	func_polynomials = [
				[(-2, 2.5), (-1, 1), (0, -4)],
				[(-2, 1.3), (0, -5)]
			]
	app(MathCore(func_polynomials=func_polynomials, mode='func'))


if __name__ == "__main__":
	start()