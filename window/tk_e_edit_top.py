from tkinter import Frame, Button, E, W, messagebox

from engine.engine_main import Game
from exceptions import ExistingRelationsError, ElementNotSet
from window.tk_e_edit_popup import NewPopup, SavePopup, InitScenePopup, ScenarioNameAuthorPopup
from window.tk_settings import lang, functions


class TopMenu(Frame):
    def __init__(self, _master_: Frame, _game_: Game):
        super().__init__(master=_master_, bg='grey', height=50)
        self._game = _game_
        self._build()
        pass

    def resize(self):
        width = self.master.winfo_width()
        self.config(width=width)
        self._new_element.place(anchor=E, rely=0.25, x=width - 5, height=23, width=150)
        self._del_element.place(anchor=E, rely=0.75, x=width - 5, height=23, width=150)
        self._scene_default.place(anchor=E, rely=0.25, x=width - 165, height=23, width=150)
        self._name_author.place(anchor=E, rely=0.75, x=width - 165, height=23, width=150)
        pass

    def _build(self):
        self.place(in_=self.master)

        self._new_element = Button(self, text=lang['tm_add'], command=self._new)
        self._del_element = Button(self, text=lang['tm_del'], command=self._del)
        self._scene_default = Button(self, text=lang['tm_scene'], command=self._scene)
        self._name_author = Button(self, text=lang['tm_name_author'], command=self._name_author_edit)

        self._save_game = Button(self, text=lang['tm_save'], command=self._save)
        self._save_game.place(anchor=W, rely=0.25, x=5, height=23, width=150)
        self._close_game = Button(self, text=lang['tm_close'], command=self._exit)
        self._close_game.place(anchor=W, rely=0.75, x=5, height=23, width=150)
        pass

    def _new(self):
        NewPopup(self._game)
        pass

    def _del(self):
        if functions['current_element']() is None:
            messagebox.showerror(message=lang['tm_error_no_element'])
            return
        elif messagebox.askokcancel(message=lang['tm_ask_delete']):
            try:
                functions['remove_element']()
                pass
            except ExistingRelationsError:
                if messagebox.askokcancel(message=lang['tm_ask_del_force']):
                    functions['remove_element'](_force_=True)
                    pass
                pass
            except ElementNotSet:
                messagebox.showerror(message=lang['tm_error_no_element'])
                pass
            pass
        pass

    def _scene(self):
        InitScenePopup(self._game)
        pass

    def _name_author_edit(self):
        ScenarioNameAuthorPopup(self._game)
        pass

    def _save(self):
        text = ''
        if self._game.name is None:
            text += f'{lang["tm_none_name"]}\n'
            pass
        if self._game.author is None:
            text += f'{lang["tm_none_author"]}\n'
            pass
        if self._game.scene is None:
            text += f'{lang["tm_none_scene"]}\n'
            pass
        if len(text) == 0:
            SavePopup(self._game)
            pass
        else:
            messagebox.showerror(message=text)
        pass

    def _exit(self):
        if self._game.saved or messagebox.askokcancel(message=lang['tm_ask_close']):
            functions['close_game']()
            pass
        pass

    pass
