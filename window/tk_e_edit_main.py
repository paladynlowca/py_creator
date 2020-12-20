from tkinter import Frame, Label, Widget, LEFT, Button, E
from typing import Dict, Optional, List

from tkscrolledframe import ScrolledFrame

from constans import *
from data_frame import ElementFrame
from engine.engine_element import Code
from window.tk_e_edit_popup import TextPopup, IntPopup, BoolPopup, SinglePopup, MultiPopup, SelectPopup
from window.tk_e_item import Item
from window.tk_settings import lang


class TkEditorElement(ScrolledFrame):
    class _Property(Frame):
        def __init__(self, _master_: Frame, _name_: str, _value_, _type_: str):
            super().__init__(master=_master_, width=490, height=35, bg='darkgray')
            self.master = _master_
            self._name = lang[_name_]
            self._value = 'gen_true' if _value_ is True else 'gen_false' if _value_ is False else _value_
            self._type = _type_

            self._container: Optional[Frame] = None
            self._name_label: Optional[Label] = None
            self._value_field: Optional[Label, Frame] = None
            self._value_list: List[Item] = list()
            self._input_field: Optional[Widget] = None
            self._change: Optional[Button] = None
            self._list_end = 0
            pass

        def build(self, _position_):
            self.place(in_=self.master, x=20, y=_position_ + 25)
            self.update()
            self._container = Frame(master=self, bg='darkgray', borderwidth=1, relief="solid",
                                    width=self.winfo_width() - 100)
            self._name_label = Label(master=self.master, text=self._name, bg='darkgray')

            if self._type.startswith(('view', 'text', 'int', 'bool')):
                if self._value in lang:
                    self._value = lang[self._value]
                    pass
                self._value_field = Label(master=self, text=self._value, bg='darkgray', wraplength=365, justify=LEFT)
                if self._type.endswith('_'):
                    subs = self._type.split('_', 1)
                    self._change = Button(master=self, text=lang['mp_change'])
                    self._change.place(in_=self, anchor=E, rely=0.5, relx=1, width=80)
                pass
            elif self._type.startswith(('list', 'single')):
                self._value_field = Frame(master=self, bg='darkgray', width=365, height=25)
                self._value_field.update()
                position = 0
                row = 0
                for item_code in self._value:
                    item = Item(self._value_field, item_code)
                    item.update()
                    self._value_list.append(item)
                    position = position + 10 + item.winfo_width()
                    item.place(in_=self._value_field, x=position, y=5 + row * 20)
                    pass
                pass
            elif self._type.startswith('select'):
                self._value_field = Label(master=self, text=lang[self._value], bg='darkgray', wraplength=365)
                pass
            if not self._type.startswith('view'):
                self._change = Button(master=self, text=lang['mp_change'])
                self._change.place(in_=self, anchor=E, rely=0.5, relx=1, width=80)
                pass

            self._container.place(in_=self, relheight=1)
            self._name_label.place(in_=self, y=-15, x=5)
            self._value_field.place(in_=self, y=7, x=13)
            self._value_field.update()
            height = self._value_field.winfo_height() + 14
            self.config(height=height)
            return height + 25 + _position_

        def bind_button(self, _code_: Code, _value_):
            def create_popup(_event_):
                if self._type.startswith('text'):
                    TextPopup(_code_, self._type[self._type.find('_') + 1:], _value_)
                    pass
                elif self._type.startswith('int'):
                    IntPopup(_code_, self._type[self._type.find('_') + 1:], _value_)
                    pass
                elif self._type.startswith('bool'):
                    BoolPopup(_code_, self._type[self._type.find('_') + 1:], _value_)
                    pass
                elif self._type.startswith('single'):
                    SinglePopup(_code_, self._type[self._type.find('_') + 1:], _value_)
                    pass
                elif self._type.startswith('list'):
                    MultiPopup(_code_, self._type[self._type.find('_') + 1:], _value_)
                    pass
                elif self._type.startswith('select'):
                    SelectPopup(_code_, self._type[self._type.find('_') + 1:], _value_, self._name)
                    pass
                pass

            if self._change is not None:
                self._change.bind("<Button-1>", create_popup)
                pass
            pass

        def _resize_list(self):
            position = 0
            row = 0
            for item in self._value_list:
                item.place(in_=self._value_field, x=position, y=2 + row * 25)
                position = position + 5 + item.winfo_width()
                pass
            pass

        def resize(self, _width_: int):
            self._value_field.update()
            self.config(width=_width_ - 56, height=self._value_field.winfo_height() + 14)
            self._container.config(width=_width_ - 156)
            self._value_field.config(**{'wraplength' if type(self._value_field) is Label else 'width': _width_ - 180})
            if type(self._value_field) is Frame:
                self._resize_list()
                pass

            pass

        pass

    def __init__(self, _master_: Frame, _data_frame_: ElementFrame):
        super().__init__(master=_master_, bg='darkgray', borderwidth=2, relief="groove", scrollbars="vertical")
        self._main_frame: Frame = self.display_widget(Frame)
        self._main_frame.config(bg='darkgray')
        self._master = _master_
        self._data_frame = _data_frame_
        self.code = Code(_data_frame_.code, _data_frame_.type)
        self._end_position = 0
        self._properties: Dict[str, TkEditorElement._Property] = dict()
        self._fields: list = [('mp_id', self._data_frame.code, 'view'),
                              ('mp_type', self._data_frame.type, 'view')]
        self._type = self._data_frame.type
        self._fields_build()
        self._build()
        pass

    def _fields_build(self):
        while None in self._data_frame.relations:
            self._data_frame.relations.remove(None)
            pass
        if self._type == SCENE:
            self._fields.extend([('mp_title', self._data_frame.properties['_title_'], 'text__title_'),
                                 ('mp_desc', self._data_frame.properties['_description_'], 'text__description_'),
                                 ('mp_options', [option for option in self._data_frame.relations if
                                                 option.type == OPTION], 'list_' + OPTION)])
            pass
        elif self._type == OPTION:
            self._fields.extend([('mp_text', self._data_frame.properties['_text_'], 'text__text_'),
                                 ('mp_actions', [action for action in self._data_frame.relations if
                                                 action.type == ACTION], 'list_' + ACTION),
                                 ('mp_conditions', [condition for condition in self._data_frame.relations if
                                                    condition.type == CONDITION], 'list_' + CONDITION)])
            pass
        elif self._type == ACTION:
            self._fields.extend([('mp_sub_type', self._data_frame.properties['_precise_type_'], 'view'),
                                 ('mp_time_increase', self._data_frame.properties['_time_increase_'],
                                  'int__time_increase_'),
                                 ('mp_conditions', [condition for condition in self._data_frame.relations if
                                                    condition.type == CONDITION], 'list_' + CONDITION)])
            if self._data_frame.properties['_precise_type_'] == TARGET_ACTION:
                self._fields.append(('mp_scene', [scene for scene in self._data_frame.relations
                                                  if scene.type == SCENE], 'single_' + SCENE))
                pass
            elif self._data_frame.properties['_precise_type_'] == VARIABLE_ACTION:
                type_ = 'int' if self._data_frame.properties['_precise_type_'] == INT_VARIABLE else 'bool'
                self._fields.extend([('mp_change_type', self._data_frame.properties['_change_type_'],
                                      f'select_{type_}__change_type_'),
                                     ('mp_change_value', self._data_frame.properties['_change_value_'],
                                      f'{type_}__change_value_'),
                                     ('mp_variable', [variable for variable in self._data_frame.relations if
                                                      variable.type == VARIABLE], 'single_' + VARIABLE)])
                pass
            pass
        elif self._type == CONDITION:
            type_str = self._data_frame.properties['_precise_type_']
            type_ = 'int' if type_str == INT_CONDITION else 'bool' if type_str == BOOL_CONDITION else 'choose'
            self._fields.extend([('mp_sub_type', self._data_frame.properties['_precise_type_'], 'view'),
                                 ('mp_test_type_', self._data_frame.properties['_test_type_'],
                                  f'select_{type_}__test_type_')])
            if type_ == 'choose':
                self._fields.extend([('mp_conditions', [condition for condition in self._data_frame.relations if
                                                        condition.type == CONDITION], 'list_' + CONDITION)])
                pass
            else:
                self._fields.extend([('mp_expected_value_', self._data_frame.properties['_expected_value_'],
                                      f'{type_}__expected_value_'),
                                     ('mp_variable', [variable for variable in self._data_frame.relations if
                                                      variable.type == VARIABLE], 'single_' + VARIABLE)])
                pass
            pass
        elif self._type == VARIABLE:
            type_str = self._data_frame.properties['_precise_type_']
            type_ = 'int' if type_str == INT_CONDITION else 'bool'
            self._fields.extend([('mp_sub_type', self._data_frame.properties['_precise_type_'], 'view'),
                                 ('mp_value', self._data_frame.properties['_value_'], f'{type_}__value_'),
                                 ('mp_conditions', [condition for condition in self._data_frame.relations if
                                                    condition.type == CONDITION], 'list_' + CONDITION),
                                 ('mp_actions', [action for action in self._data_frame.relations if
                                                 action.type == ACTION], 'list_' + ACTION)])
            if type_ == 'int':
                self._fields.extend([('mp_default_increase', self._data_frame.properties['_value_'],
                                      f'{type_}__value_'),
                                     ('mp_min', self._data_frame.properties['_min_'], f'{type_}__min_'),
                                     ('mp_max', self._data_frame.properties['_max_'], f'{type_}__max_')])
                pass
            pass

        pass

    def resize(self):
        width = self._master.winfo_width()
        height = self._master.winfo_height()
        self.config(width=width - 274, height=height - 120)
        self._main_frame.config(width=width - 274, height=max(height - 120, self._end_position + 10))
        for element in self._properties:
            self._properties[element].resize(width - 254)
        pass

    def _build(self):
        for property_ in self._fields:
            if property_[0] == 'mp_change_value' and self._data_frame.properties['_change_type_'] == 'variable_inverse':
                continue
            self._properties[property_[0]] = self._Property(self._main_frame, *property_)
            pass
        for element in self._properties:
            self._end_position = self._properties[element].build(self._end_position)
            code = Code(self._data_frame.code, self._type)
            self._properties[element].bind_button(code, self._properties[element]._value)
        pass

    pass
