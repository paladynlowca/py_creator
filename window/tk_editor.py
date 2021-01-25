from time import time_ns
from tkinter import Frame, Tk, Widget
from typing import Union, Optional

from engine.engine_main import Game
from window.tk_e_edit import TkEditorEdit
from window.tk_e_popup import TkEditorNameAuthorPopup
from window.tk_menu import TkMainMenu
from window.tk_settings import register_function, init
from xml_handler.xml_loader import XMLLoader


class TkEditor(Frame):
    def __init__(self, _master_: Tk):
        super().__init__(master=_master_, bg='gray', width=1000, height=700)
        init('_edit')
        register_function('close_game', self._close_game)
        register_function('new_game', self._build_game)
        self._master = _master_
        self._game: Optional[Game] = None
        self.place(in_=self._master, x=0, y=0)

        self._previous_time = 0

        self._menu = TkMainMenu(self, True)
        self._editor = None

        self._active: Optional[TkMainMenu, TkEditorEdit] = None
        self._to_menu()
        pass

    def _change_active_frame(self, _frame_: Widget):
        if self._active is not None:
            self._active.place_forget()
            pass
        self._active = _frame_
        self._active.place()

    def _to_menu(self):
        self._change_active_frame(self._menu)
        pass

    def _to_editor(self):
        self._change_active_frame(self._editor)
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
            self.wait_window(TkEditorNameAuthorPopup(_game_=self._game, _new_=True))
            if self._game.author is None or self._game.name is None:
                self._game.close()
                self._game = None
                return
            pass
        self._editor = TkEditorEdit(self, self._game)
        self._to_editor()
        pass

    def _close_game(self):
        self._to_menu()
        if self._game is not None:
            self._game.close()
            del self._game
            self._game = None
            self._editor.destroy()
            self._editor = None
            pass
        pass

    pass
