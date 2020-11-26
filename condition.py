from typing import Union, Tuple

from constans import *
from element import Element, Code


class Condition (Element):

    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = CONDITION
        pass

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if _passive_ and _code_.type == TRIGGER:
            self._relations.add(_code_)
            return True
        return False
        pass

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if _passive_ and _code_.type == TRIGGER and _code_ in self._relations:
            self._relations.remove(_code_)
            return True
        return False
        pass

    def __bool__(self):
        return True
