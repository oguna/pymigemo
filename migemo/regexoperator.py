from enum import Enum
from typing import Optional


class RegexOperator:
    def __init__(self, _or: str, nest_in: str, nest_out: str, select_in: str, select_out: str, newline: Optional[str]):
        self._or = _or
        self.nest_in = nest_in
        self.nest_out = nest_out
        self.select_in = select_in
        self.select_out = select_out
        self.newline = newline


class RegexOperators(Enum):
    DEFAULT = RegexOperator('|', '(', ')', '[', ']', None)
    VIM_NONEWLINE = RegexOperator('\\|', '\\%(', '\\)', '[', ']', None)
    VIM_NEWLINE = RegexOperator('\\|', '\\%(', '\\)', '[', ']', '\\_s*')
    EMACS_NONEWLINE = RegexOperator('\\|', '\\(', '\\)', '[', ']', None)
    EMACS_NEWLINE = RegexOperator('\\|', '\\(', '\\)', '[', ']', '\\s-*')
