from time import time_ns
from tkinter import Frame, Tk, Widget
from typing import Union, Optional

from engine.engine_main import Game
from window.tk_e_edit import TkEditorEdit
from window.tk_e_edit_popup import ScenarioNameAuthorPopup
from window.tk_e_edit_top import TopMenu
from window.tk_e_main import TkEditorMain
from window.tk_settings import register_function, init
from xml_handler.xml_loader import XMLLoader


class TkEditorFrame(Frame):
    def __init__(self, _master_: Tk):
        super().__init__(master=_master_, bg='gray')
        init()
        register_function('close_game', self._close_game)
        register_function('new_game', self._build_game)
        self._master = _master_
        self._game: Optional[Game] = None
        self.place(in_=self._master, x=0, y=0)

        self._previous_time = 0

        self._menu = TkEditorMain(self)
        self._editor = None
        self._top_menu = None

        self._active: Optional[Union[TkEditorMain, TkEditorEdit]] = None

        self._master.bind("<Configure>", self._resize)
        self._to_menu()
        self._resize(_force_=True)
        pass

    def _resize(self, _event_=None, _force_: bool = False):

        if (time_ns() - self._previous_time) < 1000 and not _force_:
            self._previous_time = time_ns()
            return
        self._previous_width = self._master.winfo_width()
        self._previous_height = self._master.winfo_height()
        if self._active is not None:
            self._active.resize()
            pass
        if self._top_menu is not None:
            self._top_menu.resize()
            pass
        self.config(width=self._previous_width, height=self._previous_height)
        pass

    def _change_sub_frame(self, _frame_: Widget):
        if self._active is not None:
            self._active.place_forget()
            pass
        self._active = _frame_
        self._active.place()

    def _to_menu(self):
        self._change_sub_frame(self._menu)
        self._resize(_force_=True)
        pass

    def _to_editor(self):
        self._change_sub_frame(self._editor)
        self._resize(_force_=True)
        pass

    def _game_already_opened(self):
        if self._editor is not None:
            self._editor.destroy()
            pass
        self._game.close()
        del self._game
        pass

    def _build_game(self, _name_: str):
        if self._game is not None:
            self._game_already_opened()
            pass
        self._game = Game(False)
        if _name_ is not None:
            loader = XMLLoader(self._game, _name_)
            loader.load()
            self._game.saved = True
            pass
        else:
            self.wait_window(ScenarioNameAuthorPopup(_game_=self._game, _new_=True))
            if self._game.author is None or self._game.name is None:
                self._game.close()
                self._game = None
                return
            pass
        self._editor = TkEditorEdit(self, self._game)
        self._top_menu = TopMenu(self, self._game)
        self._to_editor()
        pass

    def _close_game(self):
        self._to_menu()
        if self._game is not None:
            self._game.close()
            del self._game
            self._game = None
            self._editor.destroy()
            self._top_menu.destroy()
            self._top_menu = None
            self._editor = None
            pass
        pass

    pass
