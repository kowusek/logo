from src.context import *
from src.parser_types import *
from src.visitor import *
from src.draw.canvas import *
import logging

def _return(visitor:visitor, canv: TurtlePaths, value: value=None):
    if value:
        visitor.return_val.append(value)
    visitor.is_return = True

def _print(visitor:visitor, canv: TurtlePaths, *args):
    s = str()
    for arg in args:
        s += str(arg)
        s += " "
    logging.info(f"{s}")

def _forward(visitor:visitor, canv: TurtlePaths, value: int):
    if canv:
        canv.forward(0,value)

def _backward(visitor:visitor, canv: TurtlePaths, value: int):
    if canv:
        canv.forward(0,-value)

def _left(visitor:visitor, canv: TurtlePaths, value: int):
    if canv:
        canv.rotate(0,value)

def _right(visitor:visitor, canv: TurtlePaths, value: int):
    if canv:
        canv.rotate(0,-value)

special_function = {
    "return": _return,
    "print": _print,
    "forward" : _forward,
    "backward" : _backward,
    "left" : _left,
    "right" : _right
}