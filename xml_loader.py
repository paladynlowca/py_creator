from parse_elements import *
from xml_constants import *

PARSERS: Dict[str, type] = {SCENE: ParseScene, OPTION: ParseOption, ACTION: ParseAction, CONDITION: ParseCondition,
                            VARIABLE: ParseVariable}


class XMLLoader:
    def __init__(self, _game_: Game, _scenario_name_: str):
        self._format = 'py_creator'
        self._version = '0.1'
        self._game = _game_
        self._file: str = f'scenarios/{_scenario_name_}.xml'
        self._root: ElementTree.Element = ElementTree.parse(self._file).getroot()
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
                print(type_)
                print('ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
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
        self._game.change_scene(Code('hall', SCENE))
        pass

    pass


game = Game()
parser = XMLLoader(game, 'test2')
parser.load()
# game.add_relation(Code('hall', SCENE), Code('to_entry', OPTION))
scene = game.scene
print(scene.title)
print(scene.options)
