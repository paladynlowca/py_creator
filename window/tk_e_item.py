from tkinter import Frame, Label

from engine.engine_element import Code
from window.tk_settings import functions


class Item(Label):
    def __init__(self, _master_: Frame, _code_: Code):
        super().__init__(_master_, bg='lightgray', text=_code_.code, borderwidth=2, relief="groove", cursor="hand2",
                         width=len(_code_.code) + 2)

        self._code = _code_
        self.bind("<Enter>", self._on_entry)
        pass

    def _on_entry(self, _event_):
        functions['on_item'](self._code)
        pass

    pass
