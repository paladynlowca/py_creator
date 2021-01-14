from copy import copy
from typing import List, Optional

from constans import *
from data_frame import ElementFrame
from engine.engine_element import Code, ConditionUsing


class Option(ConditionUsing):
    """
    Scene option.
    """

    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._type = OPTION
        self._actions: List[Code] = list()
        self._text: Optional[str] = None
        self._relations_passive.add(SCENE)
        pass

    @property
    def actions(self) -> List[Code]:
        """
        Actions property.
        :return: All option actions.
        :rtype: list
        """
        return copy(self._actions)

    @property
    def text(self):
        """
        Text property.
        :return: Text value.
        :rtype: str
        """
        return self._text

    @property
    def element_frame(self):
        frame = ElementFrame(_text_=self.text)
        frame.add_relation(*self._conditions, *self.actions)
        return frame

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
        if self.code == Code('__game_over__', OPTION) and not _passive_:
            return False
        if not _passive_:
            if _code_.type == ACTION:
                return self._list_append(_code_, self._actions)
            pass
        return super().add_relation(_code_, _passive_)

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
        if not _passive_:
            if _code_.type == ACTION:
                return self._list_remove(_code_, self._actions)
            pass
        return super().del_relation(_code_, _passive_)

    def build(self, _text_: Optional[str] = None):
        """
        Building option object.
        :param _text_: Text displayed as scene option in UI.
        :type _text_: str
        """
        if _text_:
            self._text = _text_
            pass
        pass
    pass
