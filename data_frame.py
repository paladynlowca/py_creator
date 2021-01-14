from pathlib import Path
from typing import Dict, Optional, List

from engine.engine_element import Code


class ElementFrame:
    def __init__(self, **kwargs):
        self.code = None
        self.type = None
        self.properties: Dict[str,] = dict()
        self.relations: List[Code] = list()

        for attribute in kwargs:
            self.add_property(attribute, kwargs[attribute])
            pass
        pass

    def add_property(self, _name_: str, _value_):
        if _name_ == 'code':
            self.code = _value_
            return
        if _name_ == 'type':
            self.type = _value_
            return
        self.properties[_name_] = _value_
        pass

    def add_relation(self, *args):
        for element in args:
            self.relations.append(element)
            pass
        pass

    def __eq__(self, other):
        if type(other) in (type(self), Code) and other.code == self.code and other.type == self.type:
            return True
        return False

    def __str__(self):
        return f'ElementFrame with code >{self.code}< and type >{self.type}<.'

    def __repr__(self):
        return self.__str__()

    pass


class SceneFrame:
    """
    Class contains all data use for display scene.
    """

    def __init__(self, _code_: Code, _title_: Optional[str] = None, _describe_: Optional[str] = None):
        """
        :param _title_: Scene title.
        :type _title_: str
        :param _describe_: Scene describe.
        :type _describe_: str
        :param _img_: Scene image path.
        :type _img_: Path
        """
        self.code = _code_
        self.title: Optional[str] = _title_
        self.describe: Optional[str] = _describe_
        self.options: Dict[Code, str] = dict()
        pass

    def add_option(self, _code_: Code, _text_: str) -> bool:
        """
        Adding option to scene.
        :param _code_: Option code.
        :type _code_: Code
        :param _text_: Option text.
        :type _text_: str
        :return: Success of operation.
        :rtype: bool
        """
        if _code_ not in self.options:
            self.options[_code_] = _text_
            return True
        return False
    pass
