"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

BASIS = ["bspline", "fourier"]
GROUP = ["LBMP", "wind"]
CONSTRAINT = ["none", "second_derivative", "harmonic"]

__all__ = ["BLD", "SRC", "TEST_DIR", "BASIS", "GROUP", "CONSTRAINT"]
