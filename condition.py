from abc import abstractmethod
from typing import Optional

from constans import *
from element import Code, ConditionUsing
from exceptions import *


class Condition(ConditionUsing):

    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type: str = CONDITION
        self._condition_type: Optional[type] = None
        self._condition_type_str: Optional[str] = None
        self._relations_passive.update({ACTION, VARIABLE, OPTION, CONDITION})

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

    @variable.setter
    def variable(self, _value_: Code):
        if _value_.type == VARIABLE:
            self._variable = _value_
            pass
        pass

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
        return super().add_relation(_code_, _passive_)

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_:
            if _code_.type == VARIABLE:
                return self._property_remove(_code_, VARIABLE)
            pass
        return super().del_relation(_code_, _passive_)

    def _retype(self, _value_):
        try:
            return self._condition_type(_value_)
            pass
        except (ValueError, TypeError):
            raise TypeCollisionError(self.code.code, self._condition_type.__name__, type(_value_).__name__)

    def _set_ready(self):
        self._ready = True if None in (self.expected, self.test_type, self._variable) else False

    def build(self, _test_type_: str = None, _expected_value_: int = None):
        if _test_type_ is not None:
            self.test_type = _test_type_
            pass
        if _expected_value_ is not None:
            self.expected = _expected_value_
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


class MultiCondition(Condition):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._condition_type = int
        self._condition_type_str = MULTI_CONDITION
        self._test_set = (None, MULTI_AND, MULTI_OR)
        pass

    def test(self, _values_: list) -> bool:
        output = True if self.test_type is MULTI_AND or not len(_values_) else False
        for value in _values_:
            if self.test_type is MULTI_AND:
                output = output and value
                pass
            elif self.test_type is MULTI_OR:
                output = output or value
                pass
            pass
        return output
        pass

    pass
