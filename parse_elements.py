from typing import Optional, Dict, List, Set
from xml.etree import ElementTree

from constans import *
from element import Code
from game import Game
from xml_constants import *


class ParseElement:
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        self._element: ElementTree.Element = _element_
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
                self._kwargs[self._kwarg_tags[tag_type]] = value.text
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
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_TITLE: '_title_', XML_DESCRIPTION: '_description_'})
        self._relation_tags.update({OPTION})
        pass

    pass


class ParseOption(ParseElement):
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_TEXT: '_text_'})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass


class ParseAction(ParseElement):
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TIME_INCREASE: '_time_increase_',
                                   XML_CHANGE_TYPE: '_change_type_', XML_CHANGE_VALUE: '_change_value_'})
        self._relation_tags.update({OPTION, CONDITION})
        pass

    pass


class ParseCondition(ParseElement):
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TEST_TYPE: '_test_type_',
                                   XML_EXPECTED_VALUE: '_expected_value_'})
        self._relation_tags.update({VARIABLE})
        pass

    pass


class ParseVariable(ParseElement):
    def __init__(self, _element_: ElementTree.Element, _game_: Game):
        super().__init__(_element_, _game_)
        self._kwarg_tags.update(**{XML_PRECISE_TYPE: '_precise_type_', XML_TEXT: '_text_',
                                   XML_DEFAULT_INCREASE: '_default_increase_', XML_VALUE_MIN: '_value_min_',
                                   XML_VALUE_MAX: '_value_min_'})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass
