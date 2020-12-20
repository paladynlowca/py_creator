from tkinter import Tk

from engine.engine_main import Game
from window.tk_game import TkGameFrame
from xml_handler.xml_loader import XMLLoader

if __name__ == '__main__':
    game = Game()
    loader = XMLLoader(game, 'test3')
    loader.load()

    window = Tk('PyCreator')
    window.title('PyCreator')
    window.minsize(800, 600)
    main_frame = TkGameFrame(window, game)
    window.mainloop()
    pass
