from abc import abstractmethod
from typing import Optional

from constans import *
from element import Element, Code
from exceptions import *


# TODO: Add "on change".
class Condition(Element):

    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type: str = CONDITION
        self._condition_type: Optional[type] = None
        self._condition_type_str: Optional[str] = None

        self._variable: Optional[Code] = None

        self._test_set: Optional[set] = None
        self._test_type: Optional[str] = None

        self._expected = None
        self._ready = False
        pass

    @property
    def condition_type(self):
        return self._condition_type_str

    @property
    def expected(self):
        return self._expected

    @expected.setter
    def expected(self, _value_):
        self._expected = self._retype(_value_)
        self._set_ready()
        pass

    @property
    def variable(self):
        return self._variable

    @property
    def test_type(self):
        return self._test_type

    @test_type.setter
    def test_type(self, _type_: str):
        if _type_ not in self._test_set:
            raise TypeCollisionError(_type_, 'any int test type', str(_type_))
        self._test_type = _type_
        self._set_ready()
        pass

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_:
            if _code_.type == VARIABLE:
                return self._property_set(_code_, VARIABLE)
            pass
        else:
            return super().add_relation(_code_, _passive_)
        return True

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_:
            if _code_.type == VARIABLE:
                return self._property_remove(_code_, VARIABLE)
            pass
        else:
            return super().del_relation(_code_, _passive_)
        return True

    def _retype(self, _value_):
        try:
            return self._condition_type(_value_)
            pass
        except (ValueError, TypeError):
            raise TypeCollisionError(self.code.code, self._condition_type.__name__, type(_value_).__name__)

    def _set_ready(self):
        self._ready = True if None in (self.expected, self.test_type, self._variable) else False

    def build(self, _type_: str = None, _variable_: Code = None, _expected_: int = None):
        if _type_ is not None:
            self.test_type = _type_
            pass
        if _expected_ is not None:
            self.expected = _expected_
        if _variable_ is not None:
            self.expected = _expected_
            pass
        pass

    @abstractmethod
    def test(self, _value_) -> bool:
        pass

    pass


class BoolCondition(Condition):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._condition_type = bool
        self._condition_type_str = BOOL_CONDITION
        self._expected: Optional[bool] = None
        self._test_set = (None, EQUAL, DIFFERENT)
        pass

    def test(self, _value_: bool) -> bool:
        value = self._retype(_value_)
        if not self._ready:
            return False
        if self._test_type == EQUAL:
            return self._expected == value
        elif self._test_type == DIFFERENT:
            return self._expected != value
        pass

    pass


class IntCondition(Condition):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._condition_type = int
        self._condition_type_str = INT_CONDITION
        self._expected: Optional[int] = None
        self._test_set = (None, EQUAL, DIFFERENT, MORE, MORE_EQUAL, LESS, LESS_EQUAL)
        pass

    def test(self, _value_: int) -> bool:
        value = self._retype(_value_)
        if not self._ready:
            return False
        if self._test_type == EQUAL:
            return self._expected == value
        elif self._test_type == DIFFERENT:
            return self._expected != value
        elif self._test_type == MORE:
            return self._expected < value
        elif self._test_type == MORE_EQUAL:
            return self._expected <= value
        elif self._test_type == LESS:
            return self._expected > value
        elif self._test_type == LESS_EQUAL:
            return self._expected >= value
        return False

    pass
