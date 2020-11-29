from copy import copy
from typing import Set, List, Optional

from constans import *
from exceptions import *


class Code:
    def __init__(self, _code_: str, _type_: str):
        self._code = _code_
        self._type = _type_
        pass

    @property
    def code(self):
        """
        Code property.
        :return: Element str code.
        :rtype: str
        """
        return self._code
        pass

    @property
    def type(self):
        """
        Type property.
        :return: Element str type.
        :rtype: str
        """
        return self._type

    def __eq__(self, _other_):
        if type(_other_) is Code and self.code == _other_.code and self.type == _other_.type:
            return True
        return False

    def __hash__(self):
        return hash(self.code + self.type)

    def __str__(self):
        return f'Code >{self.code}< with type >{self.type}<'

    def __repr__(self):
        return f'Code({self.code}, {self.type})'
    pass


class Element:
    _codes = set()
    """
    Static set of all existing in game elements codes.
    """

    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        self._relations: Set[Code] = set()
        self._relations_passive: Set[Code] = set()
        self._type: Optional[str] = None
        self.code = _code_
        pass

    def __del__(self):
        """
        Protecting from delete element with existing relations.
        """
        if self._relations.__len__() != 0:
            relations = ''
            for relation in self._relations:
                relations += f'[{relation}]'
            raise ExistingRelationsError(self._code, self._relations)
        Element._codes.remove(self._code)

    @property
    def type(self):
        """
        Type property.
        :return: Element str type.
        :rtype: str
        """
        return self._type

    @property
    def code(self):
        """
        Code property
        :return: Element code object.
        :rtype: Code
        """
        return Code(self._code, self._type)

    @code.setter
    def code(self, _value_: str):
        """
        Code setter.
        :param _value_:
        :type _value_:
        :return:
        :rtype:
        """
        if _value_ in Element._codes:
            raise KeyError(f'Name code already exist.{_value_}')
        else:
            if '_code' in self.__dict__ and self._code is not None:
                Element._codes.remove(self._code)
                pass
            self._code = _value_
            Element._codes.add(self._code)
        pass

    @property
    def relations(self):
        """
        Relations property.
        :return: Element relations.
        :rtype: set
        """
        return self._relations

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        """
        Adding relation to element.
        :param _code_: Relation element code.
        :type _code_: Code
        :param _passive_: Type of relation - False for active, True for passive.
        :type _passive_: bool
        :return: Success of operation.
        :rtype: bool
        """
        if _passive_ and _code_.type in self._relations_passive:
            if _code_ not in self.relations:
                self._relations.add(_code_)
                pass
            return True
        return False

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        """
        Deleting relation to element.
        :param _code_: Relation element code.
        :type _code_: Code
        :param _passive_: Type of relation - False for active, True for passive.
        :type _passive_: bool
        :return: Success of operation.
        :rtype: bool
        """
        if _passive_ and _code_.type in self._relations_passive:
            if _code_ in self.relations:
                self._relations.remove(_code_)
                pass
            return True
        return False

    def check_relation(self, _code_: Code) -> bool:
        """
        Searching relations with another element.
        :param _code_: Searching element code.
        :type _code_: Code
        :return: Success of operation.
        :rtype: bool
        """
        if _code_ in self._relations:
            return True
        return False

    def _list_append(self, _code_: Code, _list_: list) -> bool:
        """
        Adding another element as active relation to multivalued list-type property.
        :param _code_: Element to add.
        :type _code_: Code
        :param _list_: List to append.
        :type _list_: list
        :return: Success of operation.
        :rtype: bool
        """
        if _code_ not in _list_:
            _list_.append(_code_)
            self._relations.add(_code_)
            return True
        return False

    def _list_remove(self, _code_: Code, _list_: list) -> bool:
        """
        Removing another, active relation, element from multivalued list-type property.
        :param _code_: Element to remove.
        :type _code_: Code
        :param _list_: List to remove from.
        :type _list_: list
        :return: Success of operation.
        :rtype: bool
        """
        if _code_ in _list_:
            _list_.remove(_code_)
            self._relations.remove(_code_)
            return True
        return False

    def _property_set(self, _code_: Code, _type_: str):
        """
        Setting active relation into single valued property.
        :param _code_: Element to add.
        :type _code_: Code
        :param _type_: Type of property.
        :type _type_: str
        :return: Success of operation.
        :rtype: bool
        """
        if self.__dict__['_' + _type_] is None:
            self.__dict__['_' + _type_] = _code_
            self._relations.add(_code_)
            return True
        return False
        pass

    def _property_remove(self, _code_: Code, _type_: str):
        """
        Removing active relation from single valued property.
        :param _code_: Element to remove.
        :type _code_: Code
        :param _type_: Type of property.
        :type _type_: str
        :return: Success of operation.
        :rtype: bool
        """
        if self.__dict__['_' + _type_] == _code_:
            self.__dict__['_' + _type_] = None
            self._relations.remove(_code_)
            return True
        return False

    pass


# Unimplemented
class ConditionUsing(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._conditions: List[Code] = list()

    @property
    def conditions(self) -> List[Code]:
        return copy(self._conditions)

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_:
            if _code_.type == CONDITION:
                return self._list_append(_code_, self._conditions)
            pass
        return super().add_relation(_code_, _passive_)

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_:
            if _code_.type == CONDITION:
                return self._list_remove(_code_, self._conditions)
            pass
        return super().del_relation(_code_, _passive_)

    def sort_conditions(self, _conditions_: List[Code]) -> bool:
        if len(self._conditions) == len(_conditions_):
            return False
        new_list = list()
        for condition in _conditions_:
            if condition in self._conditions:
                new_list.append(condition)
                pass
            else:
                return False
            pass
        self._conditions = new_list
        return True
    pass
