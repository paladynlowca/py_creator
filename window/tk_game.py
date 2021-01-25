from tkinter import Frame, Tk, messagebox
from typing import Optional, Union

from data_frame import SceneFrame
from engine.engine_element import Code
from engine.engine_main import Game
from exceptions import GameOver
from window.tk_g_menu import TkGameMainMenu
from window.tk_g_scene import TkGameScene
from window.tk_menu import TkMainMenu
from window.tk_settings import register_function, lang, init
from xml_handler.xml_loader import XMLLoader


class TkGameFrame(Frame):
    def __init__(self, _master_: Tk):
        super().__init__(master=_master_, bg='gray')
        register_function('change_scene', self._change_scene)
        register_function('new_game', self._run_game)
        init('_play')

        self._master = _master_
        self._game: Optional[Game] = None
        self._scene: Optional[TkGameScene] = None
        self._menu: Optional[TkMainMenu] = TkMainMenu(self)

        register_function('change_scene', self._change_scene)
        register_function('new_game', self._run_game)

        self.place(in_=_master_, relwidth=1, relheight=1)
        self._active: Optional[TkGameScene, TkMainMenu] = None
        self._to_menu()
        pass

    def _change_active_frame(self, _frame_: Union[TkGameScene, TkMainMenu]):
        if self._active is not None:
            self._active.place_forget()
            pass
        self._active = _frame_
        self._active.place()
        pass

    def _to_menu(self):
        self._change_active_frame(self._menu)
        pass

    def _to_scene(self):
        self._scene = TkGameScene(self, self._game.scene)
        self._change_active_frame(self._scene)
        pass

    def _run_game(self, _file_name_: str):
        if self._game is not None:
            self._game.close()
            del self._game
        self._game = Game()
        loader = XMLLoader(self._game, _file_name_)
        loader.load()
        del loader
        self._to_scene()
        pass

    def _close_game(self):
        if self._game is not None:
            self._game.close()
            del self._game
            pass
        self._game = None
        self._to_menu()
        pass

    def _change_scene(self, _code_: Code):
        try:
            self._game.execute_option(_code_)
        except GameOver:
            messagebox.showinfo(message=lang['play_game_over_popup'])
            self._close_game()
            return
        self._scene.place_forget()
        self._scene.destroy()
        self._active = None

        self._to_scene()
        pass

    pass
