from typing import Dict, Set, Tuple, Optional

from element import Element, Code
from constans import *


class Trigger(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = TRIGGER
        self._conditions: Set[Code] = set()
        self._action: Optional[Code] = None
        self._options: Optional[Code] = None
        pass

    @property
    def conditions(self):
        return self._conditions

    @property
    def action(self):
        return self._action

    @property
    def option(self):
        return self._options

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == CONDITION:
            self.add_condition(_code_)
            self._relations.add(_code_)
            pass
        elif not _passive_ and _code_.type == ACTION:
            self.add_action(_code_)
            self._relations.add(_code_)
            pass
        elif not _passive_ and _code_.type == OPTION:
            self.add_option(_code_)
            self._relations.add(_code_)
            pass
        elif _passive_ and _code_.type in {SCENE, OPTION}:
            self._relations.add(_code_)
            pass
        else:
            return False
        return True

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == CONDITION and _code_ in self._relations:
            self.add_condition(_code_)
            self._relations.remove(_code_)
            pass
        elif not _passive_ and _code_.type == ACTION and _code_ in self._relations:
            self._action = None
            self._relations.remove(_code_)
            pass
        elif not _passive_ and _code_.type == OPTION:
            self._options = None
            self._relations.remove(_code_)
            pass
        elif _passive_ and _code_.type in (SCENE, OPTION) and _code_ in self._relations:
            self._relations.remove(_code_)
            pass
        else:
            return False
        return True

    def add_condition(self, _code_: Code):
        if _code_ not in self._conditions:
            self._conditions.add(_code_)
            pass
        else:
            pass
        pass

    def add_action(self, _code_: Code):
        if _code_ != self._action:
            self._action = _code_
            pass
        else:
            pass
        pass

    def add_option(self, _code_: Code):
        if _code_ != self._action:
            self._options = _code_
            pass
        else:
            pass
        pass

    pass
