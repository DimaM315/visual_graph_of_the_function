from enum import Enum
from typing import NamedTuple, List


class GraphTypes(Enum):
	FUNC = "func"
	SEQUENCE = "seq"
	SINUSOID = "sin"


class CanvasPoint(NamedTuple):
	# point on canvas
	x: int
	y: int

class Coords(NamedTuple):
	# math calculated coords
	x: int
	y: int


class Polynom(NamedTuple):
	kf: float # koefficient on x
	dg: float # degree of x

class FunctionRepr(NamedTuple):
	numerator: List[Polynom]
	denominator: List[Polynom]

