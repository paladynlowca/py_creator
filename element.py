from abc import abstractmethod
from typing import Tuple, Union, Set

from log import log


class Code:
    def __init__(self, _code_: str, _type_: str):
        self._code = _code_
        self._type = _type_
        pass

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, _value_):
        pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _value_):
        pass

    def __eq__(self, other):
        if type(other) is Code and self.code == other.code and self.type == other.type:
            return True
        return False

    def __hash__(self):
        return hash(self.code + self.type)

    def __str__(self):
        return f'Code [{self.code}] with type [{self.type}]'

    def __repr__(self):
        return f'Code({self.code}, {self.type})'
    pass


class Element:
    _codes = set()
    __id_count = 1

    def __init__(self, _code_: str):
        self._id = Element.__id_count
        Element.__id_count += 1
        self.code = _code_
        Element._codes.add(self._code)
        self._relations: Set[Code] = set()
        self._type = None
        pass

    def __del__(self):
        if self._relations.__len__() != 0:
            relations = ''
            for relation in self._relations:
                relations += f'[{relation}]'
            raise ReferenceError(f'Deleting element [{self.code.code}] with existing relations {relations}')
        Element._codes.remove(self._code)

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def code(self):
        return Code(self._code, self._type)

    @code.setter
    def code(self, _value_: str):
        if _value_ in Element._codes:
            log('warning', f'Trying to set already existing name code. Value: {_value_}')
            raise KeyError(f'Name code already exist.{_value_}')
        else:
            self._code = _value_
        pass

    @abstractmethod
    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        pass

    @abstractmethod
    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        pass

    def check_relation(self, _code_: Code) -> bool:
        if _code_ in self._relations:
            return True
        return False

    @property
    def relations(self):
        return self._relations
    pass
