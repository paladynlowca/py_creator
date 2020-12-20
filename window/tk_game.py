from tkinter import Frame, Tk

from engine.engine_main import Game
from window.tk_g_scene import TkScenePane


class TkGameFrame(Frame):
    def __init__(self, _master_: Tk, _game_: Game):
        super().__init__(master=_master_)
        self._master = _master_
        self._game = _game_

        self.place(in_=_master_)
        self._active = TkScenePane(self, self._game.scene, self.change_scene)
        self._active.place()
        self._master.bind("<Configure>", self._resize)
        pass

    def change_scene(self, code):
        self._game.execute_option(code)

        self._active.place_forget()
        self._active.destroy()

        self._active = TkScenePane(self, self._game.scene, self.change_scene)
        self._active.place()
        self._resize(None)
        pass

    def _resize(self, _event_):
        self.config(width=self._master.winfo_width(), height=self._master.winfo_height())
        self._active.resize()
        pass

    pass
