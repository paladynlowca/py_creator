from element import Element
from log import log


class Variable (Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self.value = None
        self._type = None
        pass

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, _value_):
        try:
            value_ = self._type(_value_)
            pass
        except ValueError:
            log('error', f'Trying to set variable incorrect value. Variable: {self.code} Value: {_value_}')
            raise ValueError
            pass
        else:
            self.value = value_
        pass
    pass


class BoolVariable(Variable):
    def __init__(self, _code_: str, _value_: bool=False):
        super().__init__(_code_)
        self._type = bool
        pass

    def invert(self):
        self.value = not self.value
        pass
    pass
