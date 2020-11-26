from copy import copy

from actions import Action, TargetAction
from condition import Condition
from element import Element, Code
from exceptions import TypeCollision
from option import Option
from scene import Scene
from trigger import Trigger
from typing import Optional, Dict, Tuple, Union
from constans import *


TYPES = Union[Scene, Trigger, Condition, Action, TargetAction, Option]


class Elements(dict):
    def __init__(self):
        super().__init__()
        self._types: Dict[str, type] = {SCENE: Scene, TRIGGER: Trigger, CONDITION: Condition, ACTION: Action,
                                        TARGET_ACTION: TargetAction, OPTION: Option}
        pass

    def add_relations(self, _active_: Code, _passive_: Code):
        active = self[_active_]
        passive = self[_passive_]
        active.add_relation(_passive_, False)
        passive.add_relation(_active_)
        pass

    def del_relations(self, _active_: Code, _passive_: Code):
        active = self[_active_]
        passive = self[_passive_]
        if active.check_relation(_passive_) and passive.check_relation(_active_):
            active.del_relation(_passive_, False)
            passive.del_relation(_active_)
            pass
        pass

    def clear_relations(self, _element_: Code):
        relations = copy(self[_element_].relations)
        for relation in relations:
            self.del_relations(_element_, relation)
            self.del_relations(relation, _element_)
        pass

    def check_type(self, _code_: str) -> Optional[str]:
        if _code_ in self:
            return self[_code_].type
        return None

    def add(self, _code_: Code):
        self[_code_.code] = _code_.type

    def __setitem__(self, _code_: str, _element_: str):
        if _code_ in self:
            del self[_code_]
            pass
        if _element_ in self._types:
            _element_ = self._types[_element_](_code_)
            pass
        else:
            raise ValueError()
        super().__setitem__(_element_.code.code, _element_)
        pass

    def __getitem__(self, _key_: Union[Code, str]) -> TYPES:
        if type(_key_) is Code:
            element = super().__getitem__(_key_.code)
            if element.type == _key_.type:
                return element
            else:
                raise TypeCollision(element.code.code, element.type, _key_.type)
            pass
        else:
            return super().__getitem__(_key_)

    def __delitem__(self, _key_: str):
        element = self[_key_]
        if element.relations:
            pass
        super().__delitem__(_key_)
        pass

    def __del__(self):
        for code in self:
            self.clear_relations(self[code].code)
            pass
        pass
    pass
