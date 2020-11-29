from typing import Optional

from constans import *
from element import Element, Code


class Action(Element):
    """
    Action base class.
    """

    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._type = ACTION
        self._action_type: Optional[str] = None
        self._relations_passive.union((OPTION, VARIABLE))
        pass

    @property
    def action_type(self) -> str:
        """
        Action type property.
        :return: Type of action.
        :rtype: str
        """
        return self._action_type
    pass


class TargetAction(Action):
    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._scene: Optional[Code] = None
        self._action_type = None
        self._action_type = TARGET_ACTION
        pass

    @property
    def scene(self):
        """
        Scene property.
        :return: Target scene code.
        :rtype: Code
        """
        return self._scene

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
        if not _passive_:
            if _code_.type == SCENE:
                return self._property_set(_code_, SCENE)
            pass
        else:
            return super().add_relation(_code_, _passive_)
        return True

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
            if _code_.type == SCENE:
                return self._property_remove(_code_, SCENE)
            pass
        else:
            return super().del_relation(_code_, _passive_)
        return True
    pass
