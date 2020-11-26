from typing import Dict, Optional, Union, Any

from actions import Action
from constans import *
from element import Code
from elements import Elements, TYPES
from exceptions import TypeCollision
from data_frame import SceneFrame


class Game:
    def __init__(self):
        # List of all game elements (scenes, actions, ets).
        self._elements: Union[Dict[Any, TYPES], Elements] = Elements()
        # Switch change allow graphic game mode.
        self._allow_graphics = False  # Not fully implemented.

        # Current active scene.
        self._current_scene: Optional[Code] = None
        pass

    def create_element(self, _code_: Code) -> bool:
        """
        Creating game elements. If element with this code exist, won't change anything.
        :param _code_:
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
            type_ = SCENE
            pass
        else:
            raise TypeCollision(_code_.code, SCENE, type_)
        # Update if declared type and found type is scene type.
        if _code_.type == type_ == SCENE:
            _image_ = _image_ if self._allow_graphics else None
            self[_code_].build(_title_, _description_, _image_)
            pass
        else:
            raise TypeCollision(_code_.code, SCENE, type_)
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
            type_ = OPTION
            pass
        else:
            raise TypeCollision(_code_.code, OPTION, type_)
        # Update if declared type and found type is option type.
        if _code_.type == type_ == OPTION:
            self[_code_].build(_text_)
            pass
        else:
            raise TypeCollision(_code_.code, OPTION, type_)
        return True

    def check_trigger(self, _trigger_: str, _return_: str):
        """
        Najpewniej do przebudwoania.
        Checking all trigger conditions.
        :param _trigger_:
        :type _trigger_:
        :param _return_:
        :type _return_:
        :return:
        :rtype:
        """
        trigger = self[Code(_trigger_, TRIGGER)]
        for condition in trigger.conditions:
            if not condition:
                return None
            pass
        return trigger.action if _return_ == ACTION else trigger.option

    def close(self):
        del self._elements
        pass

    @property
    def scene(self):
        scene = self[self._current_scene]
        frame = SceneFrame(_title_=scene.title, _describe_=scene.describe, _img_=scene.image)
        for trigger in self[self._current_scene].triggers:
            option = self[self.check_trigger(trigger.code, OPTION)]
            if option:
                print(scene)
                output.append((option.text, option.code))
                pass
            pass
        return self[self._current_scene].title, self[self._current_scene].describe

    @property
    def options(self):
        output = []
        return output

    def execute(self, _option_: Code):
        for trigger in self[_option_].triggers:
            action: Action = self[self[trigger].action]
            if action.action_type == TARGET_ACTION:
                scene = self[action.code].scene
                self.change_scene(scene.code)
                pass
            pass
        pass

    def __getitem__(self, _key_: Union[Code, str]) -> TYPES:
        return self._elements[_key_]

    pass
