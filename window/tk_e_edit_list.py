from math import floor
from tkinter import Frame, NW, SW, Button
from typing import Dict, List

from tkscrolledframe import ScrolledFrame

from constans import *
from data_frame import ElementFrame
from engine.engine_element import Code
from window.tk_e_item import Item
from window.tk_settings import lang, register_function


class MyListBox(ScrolledFrame):
    def __init__(self, _master_: Frame, _on_select_):
        super().__init__(master=_master_, bg='darkgray', scrollbars="vertical")
        self.children['!canvas'].config(bg='darkgray')
        self._master = _master_
        self._on_select = _on_select_
        self._frame: Frame = self.display_widget(Frame)
        self._frame.config(bg='darkgray')
        self._frame.update()

        self._data_frames = list()
        self._items = list()
        pass

    @property
    def data_frames(self):
        return self._data_frames

    def insert(self, _frame_: ElementFrame):
        if _frame_ in self._data_frames:
            item_frame: Frame = self._items[self._data_frames.index(_frame_)]
            item_frame.children.values().__iter__().__next__().destroy()
            pass
        else:
            self._data_frames.append(_frame_)
            item_frame = Frame(master=self._frame, width=240, height=30, bg='darkgray')
            self._items.append(item_frame)
            item_frame.pack(in_=self._frame)
            pass
        item = Item(item_frame, Code(_frame_.code, _frame_.type))
        item.place(in_=item_frame, x=10, y=5)
        item.bind("<Button-1>", self._on_select_decorator(_frame_))
        pass

    def remove(self, _frame_: ElementFrame):
        try:
            index = self._data_frames.index(_frame_)
            del self._data_frames[index]
            self._items[index].destroy()
            del self._items[index]
        except ValueError:
            pass
        pass

    def _on_select_decorator(self, _frame_: ElementFrame):
        def on_select(_event_):
            self._on_select(_frame_)
            pass

        return on_select

    pass


class TkEditorSideList(Frame):
    def __init__(self, _master_: Frame, _data_frames_: List[ElementFrame], _on_select_: callable):
        super().__init__(master=_master_, bg='darkgray', borderwidth=2, relief="groove")
        self._master = _master_
        self._on_select = _on_select_
        self._type = SCENE
        self._frames: List[str] = [SCENE, OPTION, ACTION, VARIABLE, CONDITION]
        self._listboxes: Dict[str, MyListBox] = dict()
        self._build()
        self.resize()
        self.update_data(_data_frames_, list())
        register_function('get_type_frames', self._get_items)
        pass

    def resize(self):
        height = self._master.winfo_height()
        self._listbox_frame.config(height=height - 70)
        pass

    def update_data(self, _data_modified_: List[ElementFrame], _data_deleted_: List[ElementFrame]):
        for frame in _data_modified_:
            self._listboxes[frame.type].insert(frame)
            pass
        for frame in _data_deleted_:
            self._listboxes[frame.type].remove(frame)
            pass
        pass

    def _build(self):

        self._listbox_frame = Frame(master=self, height=410)
        self._listbox_frame.place(relwidth=1, y=60, anchor=NW)
        for type_ in self._frames:
            self._listboxes[type_] = self._listbox = MyListBox(self._listbox_frame, self._on_select)
            pass
        self._listbox = self._listboxes[SCENE]
        self._listbox.place(in_=self._listbox_frame, width=248, relheight=1, anchor=SW, relx=0, rely=1)

        def on_click_decorator(_type_: str):
            def change_list():
                if not self._listbox == self._listboxes[_type_]:
                    self._listbox.place_forget()
                    self._listbox = self._listboxes[_type_]
                    self._listbox.place(in_=self._listbox_frame, width=235, relheight=1, anchor=SW, relx=0, rely=1)
                    self._type = _type_
                    self.resize()
                    pass
                pass

            return change_list

        pass

        def add_button(_type_: str, _text_: str, _position_: int):
            button = Button(master=self, text=_text_, command=on_click_decorator(_type_))
            x = 5 + 75 * (_position_ % 3)
            y = floor(_position_ / 3) * 25 + 5
            button.place(in_=self, x=x, y=y, height=20, width=70)
            pass

        names = {SCENE: lang['sl_scenes'], OPTION: lang['sl_options'], ACTION: lang['sl_actions'],
                 VARIABLE: lang['sl_variables'], CONDITION: lang['sl_conditions']}
        position = 0
        for type_ in self._frames:
            add_button(type_, names[type_], position)
            position += 1
            pass
        pass

    def _get_items(self, _type_: str):
        return self._listboxes[_type_].data_frames
        pass

    pass
