from typing import Optional, Dict, Set
from xml.etree.ElementTree import Element

from constans import *
from data_frame import ElementFrame
from engine.element import Code
from xml_handler.xml_constants import *


class BuildElement:
    def __init__(self, _element_: ElementFrame):
        self._element: ElementFrame = _element_
        self._xml = Element(ELEMENT)

        self._code_str: Optional[str] = None
        self._type: Optional[str] = None
        self._code: Optional[Code] = None

        self._kwarg_tags: Dict[str, str] = dict()
        self._relation_tags: Set[str] = set()
        pass

    @property
    def xml(self):
        return self._xml

    def build(self):
        tag: Element = Element('code')
        tag.text = self._element.code
        self._xml.append(tag)
        tag = Element('type')
        tag.text = self._element.type
        self._xml.append(tag)

        for arg, value in self._element.properties.items():
            tag: Element = Element(self._kwarg_tags[arg])
            tag.text = str(value)
            self._xml.append(tag)
            pass
        for code in self._element.relations:
            if code is None:
                continue
            tag: Element = Element(code.type)
            tag.text = code.code
            self._xml.append(tag)
            pass
        pass

    pass


class BuildScene(BuildElement):
    def __init__(self, _element_: ElementFrame):
        super().__init__(_element_)
        self._kwarg_tags.update(**{'_title_': XML_TITLE, '_description_': XML_DESCRIPTION, '_image_': XML_IMAGE})
        self._relation_tags.update({OPTION})
        pass

    pass


class BuildOption(BuildElement):
    def __init__(self, _element_: ElementFrame):
        super().__init__(_element_)
        self._kwarg_tags.update(**{'_text_': XML_TEXT})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass


class BuildAction(BuildElement):
    def __init__(self, _element_: ElementFrame):
        super().__init__(_element_)
        self._kwarg_tags.update(**{'_precise_type_': XML_PRECISE_TYPE, '_time_increase_': XML_TIME_INCREASE,
                                   '_change_type_': XML_CHANGE_TYPE, '_change_value_': XML_CHANGE_VALUE})
        self._relation_tags.update({SCENE, CONDITION, VARIABLE})
        pass

    pass


class BuildCondition(BuildElement):
    def __init__(self, _element_: ElementFrame):
        super().__init__(_element_)
        self._kwarg_tags.update(**{'_precise_type_': XML_PRECISE_TYPE, '_test_type_': XML_TEST_TYPE,
                                   '_expected_value_': XML_EXPECTED_VALUE})
        self._relation_tags.update({CONDITION, VARIABLE})
        pass

    pass


class BuildVariable(BuildElement):
    def __init__(self, _element_: ElementFrame):
        super().__init__(_element_)
        self._kwarg_tags.update(**{'_precise_type_': XML_PRECISE_TYPE, '_text_': XML_TEXT, '_value_': XML_VALUE,
                                   '_default_increase_': XML_DEFAULT_INCREASE, '_min_': XML_VALUE_MIN,
                                   '_max_': XML_VALUE_MAX})
        self._relation_tags.update({ACTION, CONDITION})
        pass

    pass
