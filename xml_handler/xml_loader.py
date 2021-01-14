from typing import Dict, List
from xml.etree.ElementTree import Element, parse

from constans import *
from engine.engine_element import Code
from engine.engine_main import Game
from xml_handler.xml_constants import *
from xml_handler.xml_parse_elements import ParseScene, ParseOption, ParseAction, ParseCondition, ParseVariable, \
    ParseElement

PARSERS: Dict[str, type] = {SCENE: ParseScene, OPTION: ParseOption, ACTION: ParseAction, CONDITION: ParseCondition,
                            VARIABLE: ParseVariable}


class XMLLoader:
    def __init__(self, _game_: Game, _scenario_name_: str):
        self._format = 'py_creator'
        self._version = '0.1'
        self._game = _game_
        self._file: str = f'scenarios/{_scenario_name_}.xml'
        self._root: Element = parse(self._file).getroot()
        pass

    def load(self):
        if 'format' not in self._root.attrib or self._root.attrib['format'] != self._format:
            print('wrong data type')
            return False
        if self._root.attrib['version'] != self._version:
            print('wrong version')
            return False
        elements: List[ParseElement] = list()
        for element in self._root.findall(ELEMENT):
            type_ = element.find(XML_TYPE)
            if type_.text not in BASIC_TYPES_LIST:
                pass
            else:
                elements.append(PARSERS[type_.text](element, self._game))
                pass
            pass
        for element in elements:
            element.parse()
            element.build()
            pass
        for element in elements:
            element.add_relations()
            pass
        settings: Element = self._root.find(XML_SETTINGS)
        name: Element = settings.find(XML_NAME)
        if name is not None:
            self._game.name = name.text
            pass
        author: Element = settings.find(XML_AUTHOR)
        if author is not None:
            self._game.author = author.text
            pass
        init_scene: Element = settings.find(XML_INIT_SCENE)
        if init_scene is not None:
            self._game.change_scene(Code(init_scene.text, SCENE))
            pass
        pass

    pass
