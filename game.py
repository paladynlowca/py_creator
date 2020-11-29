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

    def build_scene(self, _code_: Code, _title_: Optional[str] = None, _description_: Optional[str] = None,
                    _image_: Optional[str] = None) -> bool:
        """
        Building new scene element, of filling already exist with new parameters.
        :param _code_: Scene code
        :type _code_: Code
        :param _title_: Scene title.
        :type _title_: str
        :param _description_: Scene description.
        :type _description_: str
        :param _image_: Scene image (only if game allows graphics).
        :type _image_: str
        :raises TypeCollision: Raises TypeCollision if declared type or found type isn't scene type.
        :return: Success of operation.
        :rtype: bool
        """
        type_ = self._elements.check_type(_code_.code)
        # Create scene if don't exist.
        if type_ is None and _code_.type == SCENE:
            self._elements.add(_code_)
            type_ = self._elements.check_type(_code_.code)
            pass
        if _code_.type != SCENE or type_ != SCENE:
            raise TypeCollisionError(_code_.code, SCENE, type_)
        # Update if declared type and found type is scene type.
        _image_ = _image_ if self._allow_graphics else None
        self[_code_].build(_title_, _description_, _image_)
        return True

    def build_option(self, _code_: Code, _text_: Optional[str] = None) -> bool:
        """
        Building new option element, of filling already exist with new parameters.
        :param _code_: Option code.
        :type _code_: Code
        :param _text_: Displayed text of option.
        :type _text_: str
        :return: Success of operation.
        :rtype: bool
        """
        type_ = self._elements.check_type(_code_.code)
        # Create option if don't exist.
        if type_ is None and _code_.type == OPTION:
            self._elements.add(_code_)
            type_ = self._elements.check_type(_code_.code)
            pass
        if _code_.type != OPTION or type_ != OPTION:
            raise TypeCollisionError(_code_.code, OPTION, type_)
        # Update if declared type and found type is option type.
        self[_code_].build(_text_)
        return True

    def build_condition(self, _code_: Code, _type_: str = None, _expected_: int = None):
        type_ = self._elements.check_type(_code_.code)
        if type_ is None and _code_.type in CONDITION_LIST:
            self._elements.add(_code_)
            type_ = self._elements.check_type(_code_.code)
            pass
        if type_ != CONDITION:
            raise TypeCollisionError(_code_.code, CONDITION, type_)
        if type_ == CONDITION:
            self[Code(_code_.code, CONDITION)].build(_type_, _expected_)
            pass
        return True

    def build_variable_action(self, _code_: Code, _change_type_: str = None, _change_value_: Union[int, bool] = None):
        type_ = self._elements.check_type(_code_.code)
        if type_ is None and _code_.type is VARIABLE_ACTION:
            self._elements.add(_code_)
            type_ = self._elements.check_type(_code_.code)
            pass
        if type_ != ACTION:
            raise TypeCollisionError(_code_.code, ACTION, type_)
        if type_ == ACTION:
            self[Code(_code_.code, ACTION)].build(_change_type_, _change_value_)
            pass
        return True

    def close(self):
        """
        Preparing to safe game exit.
        """
        del self._elements
        pass

    def execute(self, _option_: Code):
        """
        Executing all scene actions.
        :param _option_: Option choose by player.
        :type _option_: Code
        """
        if _option_.type is OPTION and _option_ in self.scene.options and self.check_conditions(_option_):
            for code in self[_option_].actions:
                action = self[code]
                if self.check_conditions(code):
                    if action.action_type == TARGET_ACTION:
                        self.change_scene(action.scene)
                        pass
                    elif action.action_type == VARIABLE_ACTION:
                        if action.change_type == VARIABLE_INCREASE:
                            self[action.variable].increase(action.change_value)
                            pass
                        elif action.change_type == VARIABLE_DECREASE:
                            self[action.variable].decrease(action.change_value)
                            pass
                        elif action.change_type == VARIABLE_SET:
                            self[action.variable].value = action.change_value
                            pass
                        elif action.change_type == VARIABLE_INVERSE:
                            self[action.variable].invert()
                            pass
                        pass
                    pass
                pass
            pass
        pass

    def check_conditions(self, _condition_: Code):
        value = True
        for condition in self[_condition_].conditions:
            if condition.type is not CONDITION:
                raise TypeCollisionError(condition.code, CONDITION, _condition_.type)
            condition_el: Condition = self[condition]
            variable = self[condition_el.variable]
            value = value and condition_el.test(variable.value)
            pass
        return value

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
