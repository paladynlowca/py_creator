from tkinter import Toplevel, Label, Text, Button, SE, N, END, WORD, INSERT, Entry, messagebox, IntVar, Radiobutton, \
    Frame, Listbox
from typing import List

from tkscrolledframe import ScrolledFrame

from constans import *
from engine.engine_element import Code
from window.tk_e_item import Item
from window.tk_settings import lang, functions


class EditPopup(Toplevel):
    def __init__(self, _code_: Code):
        super().__init__(width=500, height=300, bg='darkgray')
        self._code = _code_
        self.focus_force()
        self.grab_set()
        self.resizable(False, False)
        pass

    def _build(self):
        button = Button(master=self, text=lang['pu_confirm'], command=self._confirm)
        button.place(in_=self, anchor=SE, x=320, y=290, width=150, height=23)

        button = Button(master=self, text=lang['pu_cancel'], command=self._close)
        button.place(in_=self, anchor=SE, x=490, y=290, width=150, height=23)
        pass

    def _confirm(self):
        pass

    def _close(self):
        self.destroy()
        pass

    pass


class PropertyPopup(EditPopup):
    def __init__(self, _code_: Code, _property_: str, _value_: str):
        super().__init__(_code_)
        self._property = _property_
        self._value = '' if _value_ is None else _value_
        self.texts = None
        self._label = None
        self._input = None
        self._button = None
        pass

    def _build(self):
        self._label = Label(master=self, text=f'{lang["pu_new_value"]} {lang[self.texts[self._property]]}',
                            bg='darkgray')
        self._label.place(in_=self, x=10, y=10)

        self._input.place(in_=self, anchor=N, relx=0.5, y=30)
        self._input.insert(INSERT, self._value)
        self._input.focus_set()
        super()._build()
        pass

    def _confirm(self):
        pass


class TextPopup(PropertyPopup):
    def __init__(self, _code_: Code, _property_: str, _value_: str):
        super().__init__(_code_, _property_, _value_)
        self.texts = {'_title_': 'mp_title', '_description_': 'mp_desc', '_text_': 'mp_text'}
        self._build()
        pass

    def _build(self):
        self._input = Text(master=self, width=59, height=14, wrap=WORD)
        super()._build()
        pass

    def _confirm(self):
        data: str = self._input.get('1.0', END)
        if data.endswith('\n'):
            data = data[0:len(data) - 1]
        functions['change_value'](self._code, self._property, data)
        self.destroy()
        pass

    pass


class IntPopup(PropertyPopup):
    def __init__(self, _code_: Code, _property_: str, _value_: str):
        super().__init__(_code_, _property_, _value_)
        self.texts = {'_time_increase_': 'mp_time_increase', '_change_value_': 'mp_change_value', '_value_': 'mp_value'}
        self._build()
        pass

    def _build(self):
        self._input = Entry(master=self, width=78)
        super()._build()
        pass

    def _confirm(self):
        data = self._input.get()
        try:
            data = int(data)
            functions['change_value'](self._code, self._property, data)
            self.destroy()
            pass
        except ValueError:
            messagebox.showerror(message=lang['pu_error_int'])
            return
        pass

    pass


class BoolPopup(PropertyPopup):
    def __init__(self, _code_: Code, _property_: str, _value_: str):
        super().__init__(_code_, _property_, _value_)
        self.texts = {'_change_value_': 'mp_change_value', '_value_': 'mp_value'}
        self._variable = IntVar()
        self._build()
        pass

    def _build(self):
        self._input = Frame(master=self, width=450, height=250)
        option1 = Radiobutton(master=self._input, text=lang['gen_true'], variable=self._variable, value=1)
        option1.place(in_=self._input, x=10, y=10)
        option2 = Radiobutton(master=self._input, text=lang['gen_false'], variable=self._variable, value=0)
        option2.place(in_=self._input, x=10, y=40)
        if self._value is True:
            option1.select()
            pass
        else:
            option2.select()
            pass
        super()._build()
        pass

    def _confirm(self):
        data = bool(self._variable.get())
        functions['change_value'](self._code, self._property, data)
        self.destroy()
        pass

    pass


class ElementsPopup(EditPopup):
    def __init__(self, _code_: Code, _type_: str, _values_: List[Code]):
        super().__init__(_code_)
        self._single = True
        self._options: List[Code] = [Code(frame.code, frame.type) for frame in functions['get_type_elements'](_type_)]
        self._values: List[Code] = _values_

        self._label_selected = None
        self._label_choice = None

        self._frame_selected = None
        self._frame_choice = None

        self._added = set()
        self._deleted = set()
        pass

    def _build(self):
        self._label_selected = Label(master=self, text=f'{lang["pu_curr_elements"]}', bg='darkgray')
        self._label_selected.place(in_=self, x=10, y=10)

        container = ScrolledFrame(master=self, bg='darkgray', width=465, height=75, borderwidth=1, relief="solid",
                                  scrollbars="vertical")
        container.place(in_=self, x=10, y=30)
        self._frame_selected = container.display_widget(Frame, bg='darkgray', width=465)

        self._label_choice = Label(master=self, text=f'{lang["pu_choice_elements"]}', bg='darkgray')
        self._label_choice.place(in_=self, x=10, y=110)

        container = ScrolledFrame(master=self, bg='darkgray', width=465, height=75, borderwidth=1, relief="solid",
                                  scrollbars="vertical")
        container.place(in_=self, x=10, y=130)
        self._frame_choice = container.display_widget(Frame, bg='darkgray', width=465)

        super()._build()
        self._resize()
        pass

    def _resize(self):
        for item in self._frame_selected.children.copy():
            self._frame_selected.children[item].place_forget()
            self._frame_selected.children[item].destroy()
            pass

        def build(_list_, _frame_, _add_):
            pos_x = 0
            pos_y = 1
            for element in _list_:
                if element is None:
                    _list_.remove(None)
                    continue
                item = Item(_frame_, element)
                item.bind("<Button-1>", self._on_click_decorator(element, _add_, self._single))
                item.place(in_=_frame_, x=pos_x, y=pos_y)
                item.update()
                pos_x += item.winfo_width() + 5
                if pos_x > 480:
                    pos_y += 25
                    pos_x = 0
                    item.place(in_=_frame_, x=pos_x, y=pos_y)
                    pos_x += item.winfo_width() + 5
                    pass
                pass
            pos_y = max(75, pos_y + 25)
            _frame_.config(height=pos_y)
            return

        build(self._values, self._frame_selected, False)
        build(self._options, self._frame_choice, True)
        pass

    def _on_click_decorator(self, _code_: Code, _add_: bool, _single_: bool):
        def _on_click(_event_):
            if _add_:
                if _code_ in self._values or (_single_ and len(self._values) > 0):
                    return
                self._values.append(_code_)
                if _code_ in self._deleted:
                    self._deleted.remove(_code_)
                    pass
                else:
                    self._added.add(_code_)
                    pass
                pass
            else:
                if _code_ not in self._values:
                    return
                self._values.remove(_code_)
                if _code_ in self._added:
                    self._added.remove(_code_)
                    pass
                else:
                    self._deleted.add(_code_)
                    pass
                pass
            self._resize()
            pass

        return _on_click

    def _confirm(self):
        for code in self._deleted:
            functions['del_relation'](self._code, code)
            pass
        for code in self._added:
            functions['add_relation'](self._code, code)
            pass
        self.destroy()
        pass

    pass


class SinglePopup(ElementsPopup):
    def __init__(self, _code_: Code, _type_: str, _values_: List[Code]):
        super().__init__(_code_, _type_, _values_)
        self._build()
        pass

    pass


class MultiPopup(ElementsPopup):
    def __init__(self, _code_: Code, _type_: str, _values_: List[Code]):
        super().__init__(_code_, _type_, _values_)
        self._single = False
        self._build()
        pass

    pass


class SelectPopup(EditPopup):
    def __init__(self, _code_: Code, _type_: str, _value_: str, _name_: str, _action_=None, _cancel_=None):
        super().__init__(_code_)
        self._code = _code_
        self._value = _value_
        self._selected_name = None
        self._type = _type_
        self._type_name = _type_
        self._name = _name_
        self._action = _action_
        self._cancel = _cancel_
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._build()
        pass

    @property
    def _type(self):
        return self._type_

    @_type.setter
    def _type(self, _type_):
        types = {'int__change_type_': {lang['pu_ct_increase']: VARIABLE_INCREASE, lang['pu_ct_set']: VARIABLE_SET,
                                       lang['pu_ct_decrease']: VARIABLE_DECREASE},
                 'bool__change_type_': {lang['pu_ct_inverse']: VARIABLE_INVERSE, lang['pu_ct_set']: VARIABLE_SET},
                 'new_type': {lang[SCENE]: SCENE, lang[OPTION]: OPTION, lang[ACTION]: ACTION, lang[VARIABLE]: VARIABLE,
                              lang[CONDITION]: CONDITION},
                 'new_sub_action': {lang[VARIABLE_ACTION]: VARIABLE_ACTION, lang[TARGET_ACTION]: TARGET_ACTION},
                 'new_sub_variable': {lang[INT_VARIABLE]: INT_VARIABLE, lang[BOOL_VARIABLE]: BOOL_VARIABLE,
                                      lang[MULTI_CONDITION]: MULTI_CONDITION},
                 'new_sub_condition': {lang[INT_CONDITION]: INT_CONDITION, lang[BOOL_CONDITION]: BOOL_CONDITION}}
        self._type_ = types[_type_]
        for name in self._type_:
            if self._type_[name] == self._value:
                self._selected_name = name
                pass
            pass
        pass

    def _close(self):
        self._cancel()
        super()._close()
        pass

    def _build(self):
        self._label = Label(master=self, text=f'{lang["pu_curr_elements"]} {self._name}',
                            bg='darkgray')
        self._label.place(in_=self, x=10, y=10)

        self._selected = Label(master=self, text=self._selected_name)
        self._selected.place(in_=self, x=10, y=35)

        self._label = Label(master=self, text=lang["pu_choice_elements"],
                            bg='darkgray')
        self._label.place(in_=self, x=10, y=60)

        self._listbox = Listbox(master=self, width=100, height=len(self._type), bg='darkgrey')
        for name in self._type:
            self._listbox.insert(END, name)
        self._listbox.place(in_=self, x=10, y=85)
        self._listbox.bind("<<ListboxSelect>>", self._change_selected)
        super()._build()
        pass

    def _change_selected(self, _event_):
        self._selected_name = self._listbox.get(self._listbox.curselection()[0])
        self._selected.config(text=self._selected_name)
        pass

    def _confirm(self):
        if self._action is not None:
            if self._selected_name is None:
                messagebox.showerror(message=lang['tm_value_not_set'], master=self)
                return
            self._action(self._type[self._selected_name])
            self.destroy()
            return
        property_name = self._type_name.split('_', 1)[1]
        functions['change_value'](self._code, property_name, self._type[self._selected_name])
        self.destroy()
        pass

    pass
