from typing import Dict, Optional, Union, Any

from condition import Condition
from constans import *
from data_frame import SceneFrame
from element import Code
from elements import Elements, TYPES
from exceptions import TypeCollisionError


class Game:
    """
    Game engine class
    """

    def __init__(self):
        # List of all game elements (scenes, actions, ets).
        self._elements: Union[Dict[Any, TYPES], Elements] = Elements()
        # Switch change allow graphic game mode.
        self._allow_graphics = False  # Not fully implemented.

        # Current active scene.
        self._current_scene: Optional[Code] = None

        self.build_element(Code('__time__', VARIABLE), _precise_type_=INT_VARIABLE)
        pass

    @property
    def scene(self) -> SceneFrame:
        """
        Preparing scene data for user interface handler.
        :return: Current scene data.
        :rtype: SceneFrame
        """
        scene = self[self._current_scene]
        frame = SceneFrame(_title_=scene.title, _describe_=scene.describe, _img_=scene.image)
        for code in self[self._current_scene].options:
            option = self[code]
            if self.check_conditions(code):
                frame.add_option(code, option.text)
                pass
            pass
        return frame

    def create_element(self, _code_: Code) -> bool:
        """
        Creating game elements. If element with this code exist, won't change anything.
        :param _code_: Element to create
        :type _code_: Code
        :return: Success of operation.
        :rtype: bool
        """
        type_ = self._elements.check_type(_code_.code)
        if type_ is None:
            self._elements.add(_code_)
            return True
        else:
            return False

    def add_relation(self, _active_: Code, _passive_: Code) -> bool:
        """
        Adding relation between two elements.
        :param _active_: Active part of relation, witch use second element in some way.
        :type _active_: Code
        :param _passive_: Passive part of relation.
        :type _passive_: Code
        :return: Success of operation.
        :rtype: bool
        """
        return self._elements.add_relations(_active_, _passive_)

    def del_relation(self, _active_: Code, _passive_: Code) -> bool:
        """
        Deleting relation between two elements.
        :param _active_: Active part of relation, witch use second element in some way.
        :type _active_: Code
        :param _passive_: Passive part of relation.
        :type _passive_: Code
        :return: Success of operation.
        :rtype: bool
        """
        return self._elements.del_relations(_active_, _passive_)

    def change_scene(self, _scene_: Code) -> bool:
        """
        Changing current active scene.
        :param _scene_: New scene.
        :type _scene_: Code
        :return: Success of operation.
        :rtype: bool
        """
        try:
            self._current_scene = self[_scene_].code
            return True
        except KeyError:
            return False
        pass

    def build_element(self, _code_: Code, _precise_type_: str = None, **kwargs):
        if self._elements.check_type(_code_.code) is None and _code_.type in TYPES_LIST:
            self._elements.add(_code_ if _precise_type_ is None else Code(_code_.code, _precise_type_))
            pass
        self[_code_].build(**kwargs)
        pass

    def close(self):
        """
        Preparing to safe game exit.
        """
        del self._elements
        pass

    def execute_option(self, _option_: Code):
        """
        Executing all scene actions.
        :param _option_: Option choose by player.
        :type _option_: Code
        """
        if _option_.type is OPTION and _option_ in self.scene.options and self.check_conditions(_option_):
            for code in self[_option_].actions:
                self._execute_action(code)
            pass
        pass

    def _execute_action(self, _action_: Code):
        action = self[_action_]
        if self.check_conditions(_action_):
            if action.action_type == TARGET_ACTION:
                self.change_scene(action.scene)
                pass
            elif action.action_type == VARIABLE_ACTION:
                variable = self[action.variable]
                if action.change_type == VARIABLE_INCREASE:
                    variable.increase(action.change_value)
                    pass
                elif action.change_type == VARIABLE_DECREASE:
                    variable.decrease(action.change_value)
                    pass
                elif action.change_type == VARIABLE_SET:
                    variable.value = action.change_value
                    pass
                elif action.change_type == VARIABLE_INVERSE:
                    variable.invert()
                    pass
                else:
                    return
                for variable_action in variable.actions:
                    self._execute_action(variable_action)
                pass
            else:
                return
            self[Code('__time__', VARIABLE)].increase(_value_=action.time_increase)
            pass
        pass

    def check_conditions(self, _parent_: Code) -> bool:
        value = True
        for condition_code in self[_parent_].conditions:
            value = value and self._check_condition(condition_code)
        return value

    def _check_condition(self, _condition_: Code) -> bool:
        if _condition_.type is not CONDITION:
            raise TypeCollisionError(_condition_.code, CONDITION, _condition_.type)
        condition: Condition = self[_condition_]
        if condition.condition_type is MULTI_CONDITION:
            results = list()
            for sub_condition in condition.conditions:
                results.append(self._check_condition(sub_condition))
                pass
            return condition.test(results)
            pass
        else:
            variable = self[condition.variable]
            return condition.test(variable.value)
            pass
        pass

    def __getitem__(self, _key_: Union[Code, str]) -> TYPES:
        """
        Searching elements dictionary.
        :param _key_: Element code.
        :type _key_: Code or str
        :return: Element assigned to key
        :rtype: TYPES
        """
        return self._elements[_key_]

    pass
