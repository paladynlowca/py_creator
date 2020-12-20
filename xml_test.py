from data_frame import SceneFrame
from engine.engine_main import Game
from xml_handler.xml_loader import XMLLoader

if __name__ == '__main__':
    game = Game()
    loader = XMLLoader(game, 'test3')
    loader.load()
    scene: SceneFrame = game.scene
    while len(scene.options):
        options = list()
        print('', scene.title, scene.describe, '', sep='\n')
        i = 1
        for option in scene.options:
            options.append(option)
            print(i, ' > ', scene.options[option])
            i += 1
            pass
        data = input('>>')
        try:
            game.execute_option(options[int(data) - 1])
            pass
        except (IndexError, ValueError):
            print('error')
            pass
        scene = game.scene
        pass
    print(scene.title, scene.describe, '', sep='\n')

    game.close()
    pass
