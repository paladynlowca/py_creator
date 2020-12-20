from typing import Optional, Dict, List, Set
from xml.etree.ElementTree import Element

from constans import *
from engine.engine_element import Code
from engine.engine_main import Game
from xml_handler.xml_constants import *


def _prepare(_data_: str):
    if _data_ == 'None':
        return None
    if _data_ == 'True':
        return True
    if _data_ == 'False':
        return False
    return _data_
    pass


class ParseElement:
    def __init__(self, _element_: Element, _game_: Game):
        self._element: Element = _element_
        self._game: Game = _game_
        self._kwargs: Dict[str,] = dict()
        self._relations: List[Code] = list()

        self._code_str: Optional[str] = None
        self._type: Optional[str] = None
        self._code: Optional[Code] = None

        self._kwarg_tags: Dict[str, str] = dict()
        self._relation_tags: Set[str] = set()
        pass

    def parse(self):
        self._code_str = self._element.find(XML_CODE).text
        self._type = self._element.find(XML_TYPE).text
        self._code = Code(self._code_str, self._type)
        for tag_type in self._kwarg_tags:
            value = self._element.find(tag_type)
            if value is not None:
                self._kwargs[self._kwarg_tags[tag_type]] = _prepare(value.text)
                pass
            pass
        for tag_type in self._relation_tags:
            for tag in self._element.findall(tag_type):
                self._relations.append(Code(tag.text, tag.tag))
                pass
            pass
        pass

    def build(self):
        self._game.build_element(self._code, **self._kwargs)

        pass

    def add_relations(self):
        for relation in self._relations:
            self._game.add_relation(self._code, relation)
        pass

    pass


class ParseScene(ParseElement):
    def __init__(self, _element_: Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_TITLE: '_title_', XML_DESCRIPTION: '_description_', XML_IMAGE: '_image_'})
        self._relation_tags.update({OPTION})
        pass

    pass


class ParseOption(ParseElement):
    def __init__(self, _element_: Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_TEXT: '_text_'})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass


class ParseAction(ParseElement):
    def __init__(self, _element_: Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TIME_INCREASE: '_time_increase_',
                                   XML_CHANGE_TYPE: '_change_type_', XML_CHANGE_VALUE: '_change_value_'})
        self._relation_tags.update({SCENE, CONDITION, VARIABLE})
        pass

    pass


class ParseCondition(ParseElement):
    def __init__(self, _element_: Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TEST_TYPE: '_test_type_',
                                   XML_EXPECTED_VALUE: '_expected_value_'})
        self._relation_tags.update({CONDITION, VARIABLE})
        pass

    pass


class ParseVariable(ParseElement):
    def __init__(self, _element_: Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TEXT: '_text_', XML_VALUE: '_value_',
                                   XML_DEFAULT_INCREASE: '_default_increase_', XML_VALUE_MIN: '_min_',
                                   XML_VALUE_MAX: '_max_'})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass
