from os import listdir
from os.path import isfile
from tkinter import Toplevel, Button, SE, Label, Entry, DISABLED, NORMAL, messagebox, Listbox, END
from typing import Optional

from constans import *
from engine.engine_element import Code
from engine.engine_main import Game
from exceptions import *
from window.tk_e_edit_variables import SelectPopup, ElementsPopup
from window.tk_settings import lang, functions
from xml_handler.xml_saver import XMLSaver


class MenuPopup(Toplevel):
    def __init__(self, _game_: Game):
        super().__init__(width=500, height=300, bg='darkgray')
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._game = _game_
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
        self.destroy()
        pass

    def _close(self):
        self.destroy()
        pass

    pass


class NewPopup(MenuPopup):
    def __init__(self, _game_: Game):
        super().__init__(_game_)
        self._type = None
        self._sub_type = None
        self._build()
        pass

    def _build(self):
        label = Label(master=self, text=lang['mp_id'] + ':', bg='darkgray')
        label.place(in_=self, x=10, y=20)
        self._insert_id = Entry(master=self, width=55)
        self._insert_id.place(in_=self, x=150, y=20)

        label = Label(master=self, text=lang['mp_type'] + ':', bg='darkgray')
        label.place(in_=self, x=10, y=55)
        self._insert_type = Label(master=self, bg='lightgray')
        self._insert_type.place(in_=self, x=150, y=55)
        button = Button(master=self, text=lang['pu_choose'], command=self._select_type)
        button.place(in_=self, x=300, y=55)

        label = Label(master=self, text=lang['mp_sub_type'] + ':', bg='darkgray')
        label.place(in_=self, x=10, y=90)
        self._insert_sub_type = Label(master=self, bg='lightgray')
        self._insert_sub_type.place(in_=self, x=150, y=90)
        self._button_sub_type = Button(master=self, text=lang['pu_choose'], command=self._select_sub_type,
                                       state=DISABLED)
        self._button_sub_type.place(in_=self, x=300, y=90)

        super()._build()
        pass

    def _select_type(self):
        def _set(_value_: str):
            self._type = _value_
            self._insert_type.config(text=lang[_value_])
            self._insert_sub_type.config(text=None)
            if self._type in {ACTION, VARIABLE, CONDITION}:
                self._button_sub_type.config(state=NORMAL)
                pass
            else:
                self._sub_type = None
                self._button_sub_type.config(state=DISABLED)
                pass
            self.focus_force()
            self.grab_set()
            pass

        SelectPopup(Code(self._insert_id.get(), 'none'), 'new_type', '', lang['mp_type'], _set, self._sub_close)
        pass

    def _select_sub_type(self):
        def _set(_value_: str):
            self._sub_type = _value_
            self._insert_sub_type.config(text=lang[_value_])
            self.focus_force()
            self.grab_set()
            pass

        SelectPopup(Code(self._insert_id.get(), 'none'), 'new_sub_' + self._type, '', lang['mp_sub_type'], _set,
                    self._sub_close)
        pass

    def _sub_close(self):
        self.focus_force()
        self.grab_set()
        pass

    def _confirm(self):
        code = self._insert_id.get()
        if len(code) == 0 or self._type not in BASIC_TYPES_LIST or \
                (self._type == CONDITION and self._sub_type not in CONDITION_LIST) or \
                (self._type == VARIABLE and self._sub_type not in VARIABLE_LIST) or \
                (self._type == ACTION and self._sub_type not in ACTION_LIST):
            messagebox.showerror(message=lang['tm_value_not_set'])
            return
        functions['add_element'](code, self._type, self._sub_type)
        super()._confirm()
        pass

    pass


class SavePopup(MenuPopup):
    def __init__(self, _game_: Game):
        super().__init__(_game_)
        self._file_name: Optional[str] = None
        self._scenarios_path = 'scenarios/'
        self._files = list()

        self._list_file()
        self._build()
        pass

    def _build(self):
        self._label = Label(master=self, text=lang["pu_file_name"], bg='darkgray')
        self._label.place(in_=self, x=10, y=10)

        self._input = Entry(master=self, width=70)
        self._input.place(in_=self, x=10, y=35)

        self._label = Label(master=self, text=lang["pu_files_list"], bg='darkgray')
        self._label.place(in_=self, x=10, y=70)

        self._listbox = Listbox(master=self, width=70, height=len(self._files), bg='darkgrey')
        for name in self._files:
            self._listbox.insert(END, name)
        self._listbox.place(in_=self, x=10, y=95)
        self._listbox.bind("<<ListboxSelect>>", self._change_current)

        super()._build()
        pass

    def _change_current(self, _event_):
        self._input.delete(0, END)
        self._input.insert(0, self._listbox.get(self._listbox.curselection()[0]).replace('.xml', ''))
        pass

    def _list_file(self):
        for file_name in listdir(self._scenarios_path):
            if isfile(self._scenarios_path + file_name) and file_name.endswith('.xml'):
                self._files.append(file_name)
                pass
            pass
        pass

    def _confirm(self):
        file_name: str = self._input.get()
        if len(file_name) == 0:
            messagebox.showerror(message=lang['pu_no_file_name'])
            return
            pass
        for char in '/<>:"/\\|?*':
            if file_name.find(char) != -1:
                messagebox.showerror(message=lang['pu_file_invalid_symbols'] + ' /<>:"/\\|?*')
                return
                pass
            pass
        if file_name.endswith('.xml'):
            file_name -= '.xml'
        saver = XMLSaver(self._game, file_name)
        try:
            saver.prepare()
            saver.save()
            self._game.saved = True
            pass
        except DefaultSceneNotSet:
            messagebox.showerror(message=lang['pu_none_default_scene'])
        del saver
        super()._confirm()
        pass

    pass


class InitScenePopup(ElementsPopup):
    def __init__(self, _game_: Game):
        super().__init__(Code('none', 'none'), SCENE, [_game_.scene.code if _game_.scene is not None else None])
        self._game = _game_
        self._build()
        pass

    def _confirm(self):
        if len(self._added) == 1:
            self._game.change_scene(self._added.pop())
        self.destroy()
        pass


class ScenarioNameAuthorPopup(MenuPopup):
    def __init__(self, _game_: Game, _new_=False):
        super().__init__(_game_)
        self._new = _new_
        self._build()
        pass

    def _build(self):
        self._name_label = Label(master=self, text=lang["new_name"], bg='darkgray')
        self._name_label.place(in_=self, x=10, y=10)

        self._name_input = Entry(master=self, width=70)
        self._name_input.place(in_=self, x=10, y=35)

        self._author_label = Label(master=self, text=lang["new_author"], bg='darkgray')
        self._author_label.place(in_=self, x=10, y=70)

        self._author_input = Entry(master=self, width=70)
        self._author_input.place(in_=self, x=10, y=95)

        if self._game.name:
            self._name_input.insert(0, self._game.name)
            pass
        if self._game.author:
            self._author_input.insert(0, self._game.author)
            pass

        super()._build()
        pass

    def _confirm(self):
        name = self._name_input.get()
        author = self._author_input.get()
        if len(name) > 0 and len(author) > 0:
            self._game.name = name
            self._game.author = author
            super()._confirm()
            pass
        else:
            text = ''
            if self._game.name is None:
                text += f'{lang["tm_none_name"]}\n'
                pass
            if self._game.author is None:
                text += f'{lang["tm_none_author"]}\n'
                pass
            messagebox.showerror(message=text)
            return
        pass

    pass
