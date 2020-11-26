from typing import Tuple, Optional, Set

from element import Element, Code
from constans import *


class Action(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = ACTION
        self._action_type: Optional[str] = None
        self._triggers: Set[Code] = set()
        pass

    @property
    def action_type(self):
        return self._action_type

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == TRIGGER:
            self._triggers.add(_code_)
            self._relations.add(_code_)
            pass
        elif _passive_ and _code_.type == TRIGGER:
            self._relations.add(_code_)
            return True
        return False

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == TRIGGER and _code_ in self._relations:
            self._triggers.remove(_code_)
            self._relations.remove(_code_)
            pass
        elif _passive_ and _code_.type == TRIGGER and _code_ in self._relations:
            self._relations.remove(_code_)
            return True
        return False
        pass
    pass


class TargetAction(Action):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._scene: Optional[Code] = None
        self._action_type = None
        self._action_type = TARGET_ACTION
        pass

    @property
    def scene(self):
        return self._scene

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == SCENE and self._scene is None:
            self._scene = _code_
            self._relations.add(_code_)
            return True
        return super().add_relation(_code_, _passive_)

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == SCENE and _code_ in self._relations:
            self._scene = None
            self._relations.remove(_code_)
            return True
        return super().del_relation(_code_, _passive_)
    pass
