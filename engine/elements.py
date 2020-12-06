from copy import copy
from typing import Optional, Dict, Union

from constans import *
from engine.action import Action, TargetAction, VariableAction
from engine.condition import Condition, BoolCondition, IntCondition, MultiCondition
from engine.element import Code
from engine.option import Option
from engine.scene import Scene
from engine.variable import BoolVariable, IntVariable
from exceptions import *

# Short type hint for any elements types.
TYPES = Union[Scene, Condition, Action, TargetAction, Option, BoolVariable, IntVariable, VariableAction]


class Elements(dict):
    """
    List of all game elements use also for handling relations between them.
    """

    def __init__(self):
        super().__init__()
        self._types: Dict[str, type] = {SCENE: Scene, CONDITION: Condition, TARGET_ACTION: TargetAction, OPTION: Option,
                                        BOOL_VARIABLE: BoolVariable, INT_VARIABLE: IntVariable,
                                        BOOL_CONDITION: BoolCondition, INT_CONDITION: IntCondition,
                                        VARIABLE_ACTION: VariableAction, MULTI_CONDITION: MultiCondition}
        pass

    def add_relations(self, _active_: Code, _passive_: Code) -> bool:
        """
        Adding relations between two game elements.
        :param _active_: Active part of relation, witch use second element in some way.
        :type _active_: Code
        :param _passive_: Passive part of relation.
        :type _passive_: Code
        :return: Success of operation.
        :rtype: bool
        """
        active = self[_active_]
        passive = self[_passive_]
        if active.add_relation(_passive_, False):
            if passive.add_relation(_active_):
                return True
            active.del_relation(_passive_, False)
            pass
        return False

    def del_relations(self, _active_: Code, _passive_: Code) -> bool:
        """
        Deleting relations between two game elements.
        :param _active_: Active part of relation, witch use second element in some way.
        :type _active_: Code
        :param _passive_: Passive part of relation.
        :type _passive_: Code
        :return: Success of operation.
        :rtype: bool
        """
        active = self[_active_]
        passive = self[_passive_]
        if active.check_relation(_passive_) and passive.check_relation(_active_):
            if active.del_relation(_passive_, False):
                if passive.del_relation(_active_):
                    return True
                pass
            pass
        return False

    def clear_relations(self, _element_: Code):
        """
        Deleting 2-way all element relations.
        :param _element_: Element to clear.
        :type _element_: Code
        """
        relations = copy(self[_element_].relations)
        for relation in relations:
            self.del_relations(_element_, relation)
            self.del_relations(relation, _element_)
        pass

    def check_type(self, _code_: str) -> Optional[str]:
        """
        Checking type of element.
        :param _code_: Element code
        :type _code_: str
        :return: Type of element or None if not found.
        :rtype: str or None
        """
        if _code_ in self:
            return super().__getitem__(_code_).type
        return None

    def add(self, _code_: Code):
        """
        Adding element to game.
        :param _code_: Element to add.
        :type _code_: str
        """
        self[_code_.code] = _code_.type

    def __setitem__(self, _code_: str, _type_: str):
        """
        Creating new game element. If already exist any with same code, deleting it.
        :param _code_: Element str code.
        :type _code_: str
        :param _type_: Element type.
        :type _type_: str
        """
        if _code_ in self:
            del self[Code(_code_, self.check_type(_code_))]
            pass
        if _type_ in self._types:
            _type_ = self._types[_type_](_code_)
            pass
        else:
            raise TypeCollisionError(_code_, 'any', _type_)
        super().__setitem__(_type_.code.code, _type_)
        pass

    def __getitem__(self, _key_: Code) -> TYPES:
        """
        Geting game element.
        :param _key_: Element code.
        :type _key_: Code or str
        :return: Game element.
        :rtype: Element subclass
        :raises TypeCollision: If declared type and found type is different.
        """
        element = super().__getitem__(_key_.code)
        if element.type == _key_.type:
            return element
        else:
            raise TypeCollisionError(element.code.code, element.type, _key_.type)
        pass

    def __delitem__(self, _key_: Code):
        """
        Delete element from game elements.
        :param _key_: Element str code.
        :type _key_: str
        :raises ExistingRelations: If element have existing relations.
        """
        element = self[_key_]
        if element.relations:
            raise ExistingRelationsError(_key_.code, element.relations)
        super().__delitem__(_key_)
        pass

    def __del__(self):
        """
        Clearing all relations on delete.
        """
        for code in self:
            self.clear_relations(self[Code(code, self.check_type(code))].code)
            pass
        pass
    pass
