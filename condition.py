from constans import *
from element import Element


# Niezaimplementowane
class Condition (Element):

    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = CONDITION
        pass

    def __bool__(self):
        return True
