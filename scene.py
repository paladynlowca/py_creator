from copy import copy
from pathlib import Path
from typing import Tuple, Union, Optional

from element import Element, Code
from log import log
from constans import *


class Scene(Element):
    def __init__(self, _code_: str):
        super().__init__(_code_)
        self._type = SCENE

        self.title: Optional[str] = None
        self.describe: Optional[str] = None
        self._image: Optional[Path] = None

        self._triggers = list()
        pass

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, _value_: str):
        self._title = _value_
        pass

    @property
    def describe(self):
        return self._describe

    @describe.setter
    def describe(self, _value_: str):
        self._describe = _value_
        pass

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, _value_: str):
        self._image = Path(_value_)
        pass

    @property
    def triggers(self):
        return copy(self._triggers)

    def build(self, _title_: Optional[str] = None, _description_: Optional[str] = None, _image_: Optional[str] = None):
        if _title_ is not None:
            self.title = _title_
            pass
        if _description_ is not None:
            self.describe = _description_
            pass
        if _image_ is not None:
            self.image = _image_
            pass

    def add_relation(self, _code_: Code, _passive_=True) -> bool:
        if not _passive_ and _code_.type == TRIGGER:
            self.add_trigger(_code_)
            self._relations.add(_code_)
            pass
        elif _passive_ and _code_.type in {ACTION}:
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
        elif _passive_ and _code_.type in {ACTION}:
            self._relations.remove(_code_)
            pass
        else:
            return False
        return True

    def add_trigger(self, _code_: Code):
        if _code_ in self._triggers:
            log('warning', f'Trying to add same action twice time to scene.'
                           f'Action: {_code_} Scene: {self.code}')
            pass
        else:
            self._triggers.append(_code_)
        pass

    pass
