from abc import abstractmethod
from typing import Optional, Set

from constans import *
from element import Element, Code
from exceptions import *


class Variable(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._exception_on_range: bool = False
        self._type = VARIABLE
        self._value_type: Optional[type] = None
        self._value_type_str: Optional[str] = None
        self._relations_passive.update({CONDITION, ACTION})
        self._value = None
        self._actions: Set[Code] = set()
        pass

    @property
    def value_type(self):
        return self._value_type_str

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _value_):
        value = self._retype(_value_)
        if self._is_correct(value):
            self._value = value
            pass
        elif self._exception_on_range:
            raise ValueError()
        else:
            self._value = self._trim(value)
        pass

    @property
    def actions(self):
        return self._actions.copy()

    @property
    def exception_on_range(self) -> bool:
        return self._exception_on_range

    @exception_on_range.setter
    def exception_on_range(self, _value_: bool):
        self._exception_on_range = bool(_value_)

    def _retype(self, _value_):
        try:
            return self._value_type(_value_)
            pass
        except (ValueError, TypeError):
            raise TypeCollisionError(self.code.code, self._value_type.__name__, type(_value_).__name__)
        pass

    def build(self, _value_=None, **kwargs):
        if _value_ is not None:
            value = True if _value_ == 'True' else False if _value_ == 'False' else _value_
            self.value = value
            pass
        super().build(**kwargs)
        pass

    @abstractmethod
    def _is_correct(self, _value_):
        pass

    @abstractmethod
    def _trim(self, _value_):
        pass

    pass


class BoolVariable(Variable):
    def __init__(self, _code_: str, _value_: bool = False):
        super().__init__(_code_)
        self._value_type = bool
        self._value_type_str = BOOL_VARIABLE
        self.value = _value_
        pass

    def invert(self):
        self.value = not self.value
        pass

    def _is_correct(self, _value_: bool):
        if _value_ in (True, False):
            return True
        return False

    def _trim(self, _value_: bool) -> bool:
        return bool(_value_)

    pass


class IntVariable(Variable):
    def __init__(self, _code_: str, _value_: int = 0):
        super().__init__(_code_)
        self._value_type = int
        self._value_type_str: str = INT_VARIABLE
        self._default_increase: int = 1
        self._min: Optional[int] = None
        self._max: Optional[int] = None
        self.value: int = _value_
        pass

    @property
    def default_increase(self) -> int:
        return self._default_increase

    @default_increase.setter
    def default_increase(self, _value_):
        value = self._retype(_value_)
        if (self.min is None or self.max is None or value <= (self.max - self.min)) and value >= 0:
            self._default_increase = value
            pass
        elif self.exception_on_range:
            raise OutOfRangeError(value, 0, None if self.min is None or self.max is None else self.max - self.min)
        else:
            self._default_increase = self.max - self.min
        pass

    @property
    def max(self) -> Optional[int]:
        return self._max

    @max.setter
    def max(self, _value_: Optional[int]):
        if _value_ is None:
            self._max = _value_
            return
        value = int(_value_)
        if self.value <= value and (self.min is None or value >= (self.min + self.default_increase)):
            self._max = value
        else:
            if self._exception_on_range:
                min_value = self.value if self.min is None else max(self.value, (self.min + self.default_increase))
                raise OutOfRangeError(value, min_value, None)
            else:
                self._max = value
                self.value = min(value, self.value)
                pass
            pass
        pass

    pass

    @property
    def min(self) -> Optional[int]:
        return self._min

    @min.setter
    def min(self, _value_: Optional[int]):
        if _value_ is None:
            self._min = _value_
            return
        value = int(_value_)
        if self.value >= value and (self._max is None or value <= (self.max - self.default_increase)):
            self._min = value
            pass
        else:
            if self._exception_on_range:
                max_value = self.value if self.max is None else min(self.value, (self.max - self.default_increase))
                raise OutOfRangeError(value, None, max_value)
            else:
                self._min = value
                self.value = value
                pass
            pass
        pass

    def increase(self, _value_: Optional[int] = None, _reverse_: bool = False):
        multi = -1 if _reverse_ else 1
        if _value_ is None:
            value = self.default_increase
            pass
        else:
            value = self._retype(_value_)
            pass
        new_value = self.value + value * multi
        if self.exception_on_range:
            if value >= 0 and self._is_correct(new_value):
                self.value = new_value
                pass
            else:
                raise OutOfRangeError(value, self.min, self.max)
            pass
        else:
            if value >= 0:
                self.value = self._trim(new_value)
        pass

    def decrease(self, _value_: Optional[int] = None):
        self.increase(_value_, True)
        pass

    def _is_correct(self, _value_: int) -> bool:
        if (self.min is None or _value_ >= self.min) and (self.max is None or _value_ <= self.max):
            return True
        return False

    def _trim(self, _value_: int) -> int:
        return self.min if self.min is not None and _value_ < self.min \
            else self.max if self.max is not None and _value_ > self.max else _value_

    def build(self, _default_increase_=None, _value_min_=None, _value_max_=None, **kwargs):
        if _default_increase_ is not None:
            self.default_increase = _default_increase_
            pass
        if _value_min_ is not None:
            self.min = _value_min_
            pass
        if _value_max_ is not None:
            self.max = _value_max_
            pass
        super().build(**kwargs)
        pass

    pass
