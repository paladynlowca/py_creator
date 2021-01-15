import re
from os import listdir
from os.path import isfile
from tkinter import Frame, N, Button, Listbox, Scrollbar, NE, NW, DISABLED, NORMAL

from window.tk_settings import functions


class TkEditorMain(Frame):
    def __init__(self, _master_: Frame):
        super().__init__(master=_master_, bg='darkgray', borderwidth=2, relief="groove")
        self._master = _master_
        self._scenarios_path = 'scenarios/'
        self._open_function = functions['new_game']

        self._build()
        self._get_scenarios()
        self.place()
        self.resize()
        pass

    def place(self):
        self._master.update()
        super().place(in_=self._master, anchor=N, relx=0.5, y=50)
        pass

    def resize(self):
        self.config(width=700, height=600)

    def _build(self):
        self._new_button = Button(master=self, text='Nowy scenariusz', command=self._on_new)
        self._new_button.place(in_=self, width=450, height=40, anchor=N, relx=0.5, y=10)

        self._open_button = Button(master=self, text='Otwórz scenariusz', command=self._on_open, state=DISABLED)
        self._open_button.place(in_=self, width=450, height=40, anchor=N, relx=0.5, y=60)

        self._listbox_frame = Frame(master=self, width=170, height=300)
        self._listbox_frame.place(in_=self, width=550, height=480, anchor=N, relx=0.5, y=110)
        self._listbox = Listbox(self)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)
        self._listbox.place(in_=self._listbox_frame, width=530, height=480, anchor=NW, relx=0)
        self._scrollbar = Scrollbar(self, orient='vertical', command=self._listbox.yview)
        self._scrollbar.place(in_=self._listbox_frame, height=480, anchor=NE, relx=1)
        self._listbox.config(yscrollcommand=self._scrollbar.set)
        pass

    def _get_scenarios(self):
        self._scenarios = list()
        for file_name in listdir(self._scenarios_path):
            if not isfile(self._scenarios_path + file_name):
                continue
            with open(self._scenarios_path + file_name, 'r') as file:
                line = file.readline(100)
                found = re.search(r'name="(.*?)"', line)
                if found:
                    self._scenarios.append(file_name[0:len(file_name) - 4])
                    self._listbox.insert('end', f'{found.group(1)} ({file_name})')
                pass
            pass
        pass

    def _on_new(self, _event_=None):
        self._open_function(None)
        pass

    def _on_open(self, _event_=None):
        if self._listbox.curselection():
            file_path = self._scenarios[self._listbox.curselection()[0]]
            if isfile(f'{self._scenarios_path}{file_path}.xml'):
                self._open_function(file_path)
                pass
            else:
                self._open_button.config(state=DISABLED)
                self._listbox.delete(self._listbox.curselection())
            pass
        pass

    def _on_select(self, _event_=None):
        if self._listbox.curselection():
            self._open_button.config(state=NORMAL)
            pass
        else:
            self._open_button.config(state=DISABLED)
            pass
        pass

    pass
