from copy import copy
from pathlib import Path
from typing import Optional, List

from constans import *
from data_frame import ElementFrame
from engine.element import Element, Code


class Scene(Element):
    """
    Scene.
    """

    def __init__(self, _code_: str):
        """
        :param _code_: Element str code.
        :type _code_: str
        """
        super().__init__(_code_)
        self._type = SCENE

        self.title: Optional[str] = None
        self.describe: Optional[str] = None
        self._image: Optional[str] = None
        self._relations_passive.add(ACTION)

        self._options = list()
        pass

    @property
    def title(self) -> str:
        """
        Title property.
        :return: Title value.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, _value_: str):
        """
        Title setter.
        :param _value_: New title value.
        :type _value_: str
        """
        self._title = _value_
        pass

    @property
    def describe(self) -> str:
        """
        Describe property.
        :return: Describe value.
        :rtype: str
        """
        return self._describe

    @describe.setter
    def describe(self, _value_: str):
        """
        Describe setter.
        :param _value_: New describe value.
        :type _value_: str
        """
        self._describe = _value_
        pass

    @property
    def image(self) -> Path:
        """
        Image path property.
        :return: Image path.
        :rtype: Path
        """
        return self._image

    @image.setter
    def image(self, _value_: str):
        """
        Image path setter.
        :param _value_: New image path string.
        :type _value_: str
        """
        self._image = _value_
        pass

    @property
    def options(self) -> List[Code]:
        """
        Options property.
        :return: Scene options.
        :rtype: list
        """
        return copy(self._options)

    @property
    def element_frame(self):
        frame = ElementFrame(_title_=self.title, _description_=self.describe, _image_=self.image)
        frame.add_relation(*self.options)
        return frame

    def build(self, _title_: Optional[str] = None, _description_: Optional[str] = None, _image_: Optional[str] = None):
        """
        Building scene object.
        :param _title_: Scene title.
        :type _title_: str
        :param _description_: Scene description.
        :type _description_: str
        :param _image_: Scene image path.
        :type _image_: str
        """
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
            if _code_.type == OPTION:
                return self._list_append(_code_, self._options)
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
            if _code_.type == OPTION:
                return self._list_remove(_code_, self._options)
            pass
        else:
            return super().del_relation(_code_, _passive_)
        return True
    pass
