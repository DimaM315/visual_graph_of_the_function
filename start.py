from loguru import logger

from services import MathCore
from main import app
from entity_types import GraphTypes, Polynom, FunctionRepr



logger.add("logs/error.log", format="{time} | {level} | {message}", level="ERROR", compression="zip", rotation="50 KB")

#@logger.catch
def start():
	func = FunctionRepr(
			numerator=[Polynom(kf=-2, dg=2.5), Polynom(kf=-1, dg=1), Polynom(kf=0, dg=-4)], 
			denominator=[Polynom(kf=-2, dg=1.3), Polynom(kf=0, dg=-5)])

	app(MathCore(func=func, mode=GraphTypes.FUNC))


if __name__ == "__main__":
	start()