from copy import copy
from typing import List, Optional

from element import Element, Code
from constans import *


class Option(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = OPTION
        self._triggers: List[Code] = list()
        self._text: Optional[str] = None
        pass

    @property
    def triggers(self):
        return copy(self._triggers)

    @property
    def text(self):
        return self._text

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == TRIGGER:
            self.add_trigger(_code_)
            self._relations.add(_code_)
            pass
        elif _passive_ and _code_.type in {TRIGGER}:
            self._relations.add(_code_)
            pass
        else:
            return False
        return True

    def del_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == TRIGGER and _code_ in self._relations:
            self._triggers.remove(_code_)
            self._relations.remove(_code_)
            pass
        elif _passive_ and _code_.type in {TRIGGER}:
            self._relations.remove(_code_)
            pass
        else:
            return False
        return True

    def build(self, _text_: Optional[str] = None):
        if _text_:
            self._text = _text_
            pass
        pass

    def add_trigger(self, _code_: Code):
        if _code_ in self._triggers:
            pass
        else:
            self._triggers.append(_code_)
        pass
    pass
