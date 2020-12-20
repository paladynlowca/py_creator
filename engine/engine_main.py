from typing import Dict, Optional, Union, Any, List

from constans import *
from data_frame import SceneFrame
from engine.engine_el_condition import Condition
from engine.engine_element import Code
from engine.engine_elements import Elements, TYPES
from exceptions import TypeCollisionError


class Game:
    """
    Game engine class
    """

    def __init__(self, _play_only_: bool = True):
        self._play_only = _play_only_
        self._scenario_name = 'default'
        # List of all game elements (scenes, actions, ets).
        self._elements: Union[Dict[Any, TYPES], Elements] = Elements()
        # Switch change allow graphic game mode.
        self._allow_graphics = False  # Not fully implemented.
        self._saved = True
        self._updated_elements: List[Code] = list()
        self._deleted_elements: List[Code] = list()

        # Current active scene.
        self._current_scene: Optional[Code] = None

        self.build_element(Code('__time__', VARIABLE), _precise_type_=INT_VARIABLE)
        pass

    @property
    def name(self):
        return self._scenario_name

    @name.setter
    def name(self, _value_: str):
        self._scenario_name = str(_value_)

    @property
    def scene(self) -> SceneFrame:
        """
        Preparing scene data for user interface handler.
        :return: Current scene data.
        :rtype: SceneFrame
        """
        scene = self[self._current_scene]
        frame = SceneFrame(_code_=self._current_scene, _title_=scene.title, _describe_=scene.describe,
                           _img_=scene.image)
        for code in self[self._current_scene].options:
            option = self[code]
            if self._check_conditions(code):
                frame.add_option(code, option.text)
                pass
            pass
        return frame

    @property
    def saved(self):
        return self._saved

    @saved.setter
    def saved(self, _value_):
        self._saved = bool(_value_)

    def element(self, _code_: Code):
        frame = self[_code_].element_frame
        frame.add_property('code', _code_.code)
        frame.add_property('type', _code_.type)
        return frame

    def elements(self, _new_only_: bool = False):
        frames = list()
        if _new_only_:
            to_iter = self._updated_elements
            pass
        else:
            to_iter = self._elements
            pass
        for code in to_iter:
            frames.append(self.element(code))
            pass
        if _new_only_:
            deleted = list()
            for code in self._deleted_elements:
                deleted.append(code)
                pass
            frames = (frames, deleted)
            pass
        self._updated_elements.clear()
        self._deleted_elements.clear()
        return frames

    def add_relation(self, _active_: Code, _passive_: Union[Code, str]) -> bool:
        """
        Adding relation between two elements.
        :param _active_: Active part of relation, witch use second element in some way.
        :type _active_: Code
        :param _passive_: Passive part of relation.
        :type _passive_: Code
        :return: Success of operation.
        :rtype: bool
        """
        if self._play_only:
            return False
        if type(_passive_) is str:
            _passive_ = Code(_passive_, self._elements.check_type(_passive_))
            pass
        self._updated_elements.extend({_active_, _passive_})
        self.saved = False
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
        if self._play_only:
            return False
        self._updated_elements.extend({_active_, _passive_})
        self.saved = False
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

    def remove_element(self, _code_: Code, _force_: bool = False):
        if self._play_only:
            return False
        relations = self[_code_].relations
        if _force_:
            self._elements.clear_relations(_code_)
            pass
        del self._elements[_code_]
        self.saved = False
        self._deleted_elements.append(_code_)
        for element in relations:
            self._updated_elements.append(element)
        pass

    def build_element(self, _code_: Code, _precise_type_: str = None, **kwargs):
        if self._play_only:
            return False
        if self._elements.check_type(_code_.code) is None and _code_.type in TYPES_LIST:
            self._elements.add(_code_ if _precise_type_ is None else Code(_code_.code, _precise_type_))
            pass
        self._updated_elements.extend({_code_})
        self[_code_].build(**kwargs)
        self.saved = False
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
        if _option_.type == OPTION and _option_ in self.scene.options and self._check_conditions(_option_):
            for code in self[_option_].actions:
                self._execute_action(code)
            pass
        pass

    def _execute_action(self, _action_: Code):
        action = self[_action_]
        if self._check_conditions(_action_):
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

    def _check_conditions(self, _parent_: Code) -> bool:
        value = True
        for condition_code in self[_parent_].conditions:
            value = value and self._check_condition(condition_code)
        return value

    def _check_condition(self, _condition_: Code) -> bool:
        if _condition_.type != CONDITION:
            raise TypeCollisionError(_condition_.code, CONDITION, _condition_.type)
        condition: Condition = self[_condition_]
        if condition.condition_type == MULTI_CONDITION:
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
