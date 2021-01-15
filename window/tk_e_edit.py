from tkinter import Frame, NE
from typing import Optional

from data_frame import ElementFrame
from engine.engine_element import Code, ElementNotSet
from engine.engine_main import Game
from window.tk_e_edit_list import TkEditorSideList
from window.tk_e_edit_main import TkEditorElement
from window.tk_e_edit_top import TopMenu
from window.tk_settings import register_function


class TkEditorEdit(Frame):
    def __init__(self, _master_: Frame, _game_: Game):
        super().__init__(master=_master_, bg='darkgray', width=1000, height=700)
        register_function('on_item', self._on_item)
        register_function('on_item_click', self._on_item_click)
        register_function('change_value', self._game_change_value)
        register_function('add_relation', self._game_add_relation)
        register_function('del_relation', self._game_del_relation)
        register_function('remove_element', self._game_remove_current_element)
        register_function('add_element', self._game_add_element)
        register_function('current_element', self.current)

        self._master = _master_
        self._game = _game_
        self._main_panel: Optional[TkEditorElement] = None
        self._build()
        pass

    def place(self):
        self._master.update()
        super().place(in_=self._master, x=0, y=0)
        pass

    def current(self):
        if self._main_panel is not None:
            return self._main_panel.code
        pass

    def del_current(self):
        self._change_element(None)
        pass

    def _build(self):
        self._side_list = TkEditorSideList(self, self._game.elements(), self._change_element)
        self._side_list.place(in_=self, anchor=NE, relx=1, y=50, width=250, height=650)

        self._top_menu = TopMenu(self, self._game)
        pass

    def _change_element(self, _data_frame_: Optional[ElementFrame]):
        if self._main_panel is not None:
            self._main_panel.destroy()
            del self._main_panel
            self._main_panel = None
            pass
        if _data_frame_ is None:
            return
        self._main_panel = TkEditorElement(self, _data_frame_)
        self._main_panel.resize()
        self._main_panel.place(in_=self)
        pass

    def _fill_bottom_panel(self, _code_: str, _type_: str):
        pass

    def _game_add_element(self, _code_: str, _type_: str, _sub_type_: Optional[str]):
        code = Code(_code_, _type_)
        if self._game.element_type(code.code) is not None:
            return False
        self._game.build_element(code, _precise_type_=_sub_type_)
        self._change_element(self._game.element(code))
        self._side_list.update_data(*self._game.elements(_new_only_=True, _codes_only_=True))
        return True
        pass

    def _game_remove_current_element(self, _force_: bool = False):
        element = self.current()
        if element is None:
            raise ElementNotSet()
        self._game.remove_element(element, _force_)
        self._change_element(None)
        self._side_list.update_data(*self._game.elements(_new_only_=True, _codes_only_=True))
        pass

    def _game_change_value(self, _code_: Code, _key_word_: str, _new_value_):
        self._game.build_element(_code_, **{_key_word_: _new_value_})
        self._change_element(self._game.element(self.current()))
        return

    def _game_add_relation(self, _active_: Code, _passive_: Code):
        self._game.add_relation(_active_, _passive_)
        self._change_element(self._game.element(self.current()))
        pass

    def _game_del_relation(self, _active_: Code, _passive_: Code):
        self._game.del_relation(_active_, _passive_)
        self._change_element(self._game.element(self.current()))

    def _on_item(self, _code_):
        pass

    def _on_item_click(self, _code_):
        self._change_element(self._game.element(_code_))
        pass

    pass
