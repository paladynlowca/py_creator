from typing import Dict
from xml.etree.ElementTree import Element, tostring

from constans import *
from engine.engine_main import Game
from xml_handler.xml_build_element import BuildScene, BuildOption, BuildAction, BuildCondition, BuildVariable, \
    BuildElement
from xml_handler.xml_constants import *

BUILDERS: Dict[str, type] = {SCENE: BuildScene, OPTION: BuildOption, ACTION: BuildAction, CONDITION: BuildCondition,
                             VARIABLE: BuildVariable}


class XMLSaver:
    def __init__(self, _game_: Game, _scenario_name_: str):
        self._format = 'py_creator'
        self._version = '0.1'
        self._game = _game_
        self._file: str = f'scenarios/{_scenario_name_}.xml'
        self._root: Element = Element('scenario')
        pass

    def prepare(self):
        self._root.set('format', 'py_creator')
        self._root.set('version', '0.1')
        self._root.set('name', self._game.name)
        for frame in self._game.elements():
            builder: BuildElement = BUILDERS[frame.type](frame)
            builder.build()
            self._root.append(builder.xml)
            pass
        settings = Element(XML_SETTINGS)
        init_scene = Element(XML_INIT_SCENE)
        init_scene.text = self._game.scene.code.code
        settings.append(init_scene)
        scenario = Element(XML_NAME)
        scenario.text = self._game.name
        settings.append(scenario)
        self._root.append(settings)
        pass

    def save(self):
        with open(self._file, 'w', encoding='utf-8') as file:
            file.write(tostring(self._root, encoding='unicode'))
            pass
        pass

    pass
