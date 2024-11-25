from __future__ import annotations
from src.context import *
from src.parser_types import *
from src.visitor import *
from src.marker import marker
import logging

def _return(visitor:visitor, mark: marker, value: value=None):
    if value:
        visitor.return_val.append(value)
    visitor.is_return = True

def _print(visitor:visitor, mark: marker, *args):
    s = str()
    for arg in args:
        s += str(arg)
        s += " "
    logging.info(f"{s}")

def _forward(visitor:visitor, mark: marker, value: int):
    if mark:
        mark.forward(value)

def _backward(visitor:visitor, mark: marker, value: int):
    if mark:
        mark.forward(-value)

def _left(visitor:visitor, mark: marker, value: int):
    if mark:
        mark.rotate(value)

def _right(visitor:visitor, mark: marker, value: int):
    if mark:
        mark.rotate(-value)

special_function = {
    "return": _return,
    "print": _print,
    "forward" : _forward,
    "backward" : _backward,
    "left" : _left,
    "right" : _right
}