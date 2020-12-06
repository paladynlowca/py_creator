from typing import Optional, Union

from constans import *
from data_frame import ElementFrame
from engine.element import Code, ConditionUsing
from exceptions import *


class Action(ConditionUsing):
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
        self._relations_passive.update({OPTION, VARIABLE})
        self._time_increase = None
        pass

    @property
    def action_type(self) -> str:
        """
        Action type property.
        :return: Type of action.
        :rtype: str
        """
        return self._action_type

    @property
    def time_increase(self):
        return self._time_increase

    @time_increase.setter
    def time_increase(self, _value_):
        if _value_ is None:
            self._time_increase = _value_
            return
        value = int(_value_)
        if value >= 0:
            self._time_increase = value
            pass
        else:
            raise OutOfRangeError(value, 0, None)
        pass

    @property
    def element_frame(self):
        return None

    def build(self, _time_increase_: int = None, **kwargs):
        self.time_increase = _time_increase_
        pass


class TargetAction(Action):
    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._scene: Optional[Code] = None
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

    @property
    def element_frame(self):
        frame = ElementFrame(_precise_type_=self.action_type, _time_increase_=self.time_increase)
        frame.add_relation(*self._conditions, self._scene)
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
        if not _passive_:
            if _code_.type == SCENE:
                return self._property_set(_code_, SCENE)
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
            if _code_.type == SCENE:
                return self._property_remove(_code_, SCENE)
            pass
        return super().del_relation(_code_, _passive_)

    pass


class VariableAction(Action):
    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._variable: Optional[Code] = None
        self._action_type = VARIABLE_ACTION
        self._change_type: Optional[str] = None
        self._change_value = None
        pass

    @property
    def variable(self):
        return self._variable

    @property
    def change_type(self):
        return self._change_type

    @change_type.setter
    def change_type(self, _value_):
        if _value_ in VARIABLE_ACTIONS_LIST:
            self._change_type = _value_
            pass
        else:
            raise TypeCollisionError(self.code.code, VARIABLE_ACTIONS_LIST, _value_)
        pass

    @property
    def change_value(self):
        return self._change_value

    @change_value.setter
    def change_value(self, _value_):
        self._change_value = _value_
        pass

    @property
    def element_frame(self):
        frame = ElementFrame(_precise_type_=self.action_type, _time_increase_=self.time_increase,
                             _change_type_=self.change_type, _change_value_=self.change_value)
        frame.add_relation(*self._conditions, self._variable)
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
        if not _passive_:
            if _code_.type == VARIABLE:
                return self._property_set(_code_, VARIABLE)
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
            if _code_.type == VARIABLE:
                return self._property_remove(_code_, VARIABLE)
            pass
        return super().del_relation(_code_, _passive_)

    def build(self, _change_type_: str = None, _change_value_: Union[int, bool] = None, **kwargs):
        if _change_type_ is not None:
            self.change_type = _change_type_
            pass
        if _change_value_ is not None:
            self.change_value = _change_value_
            pass
        super().build(**kwargs)
        pass

    pass
