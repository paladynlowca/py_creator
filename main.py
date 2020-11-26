from constans import *
from data_frame import SceneFrame
from element import Code
from game import Game

if __name__ == '__main__':
    game = Game()
    # Tworzenie wszystkich elementów potrzebnych do działania scenariusza.
    scene1, scene2, scene3, scene4 = Code('s1', SCENE), Code('s2', SCENE), Code('s3', SCENE), Code('s4', SCENE)
    game.build_scene(scene1, _title_='Korytarz', _description_='Jesteś w dość krótkim korytarzu.')
    game.build_scene(scene2, _title_='Ganek', _description_='To zdecydowanie jest ganek, możesz wyjść na zewnątrz.')
    game.build_scene(scene3, _title_='Ulica',
                     _description_='Wyszedłeś na ulicę wprost pod nadjeżdzający walec drogowy. Umarłeś.')
    game.build_scene(scene4, _title_='Kuchnia.', _description_='Wszedłeś do kuchni. Nie ma tu nic ciekawego.')

    option1, option2, option3, option4 = Code('option1', OPTION), Code('option2', OPTION), Code('option3',
                                                                                                OPTION), Code('option4',
                                                                                                              OPTION)
    game.build_option(option1, 'Wejdź w drzwi po prawej.')
    game.build_option(option2, 'Wejdź w drzwi po lewej.')
    game.build_option(option3, 'Wróć na korytarz.')
    game.build_option(option4, 'Wyjdź na zewnątrz.')

    action1, action2, action3, action4 = Code('target1', ACTION), Code('target2', ACTION), Code('target3',
                                                                                                ACTION), Code('target4',
                                                                                                              ACTION)
    game.create_element(Code(action1.code, TARGET_ACTION))
    game.create_element(Code(action2.code, TARGET_ACTION))
    game.create_element(Code(action3.code, TARGET_ACTION))
    game.create_element(Code(action4.code, TARGET_ACTION))

    # ------------------------------------------------------------------------------------------------------------------

    # Dodawanie relacji pomiędzy obiektami, w komentarzach są kierunki przejść pomiędzy scenami.
    # Korytarz -> ganek
    game.add_relation(scene1, option1)
    game.add_relation(option1, action1)
    game.add_relation(action1, scene2)

    # Korytarz -> kuchnia
    game.add_relation(scene1, option2)
    game.add_relation(option2, action2)
    game.add_relation(action2, scene4)

    # Ganek -> korytarz
    game.add_relation(scene2, option3)
    game.add_relation(option3, action3)
    game.add_relation(action3, scene1)

    # kuchnia -> Korytarz (podpięcie porzednio zbudowanej opcji)
    game.add_relation(scene4, option3)

    # Ganek -> Ulica
    game.add_relation(scene2, option4)
    game.add_relation(option4, action4)
    game.add_relation(action4, scene3)

    game.change_scene(scene1)

    # ------------------------------------------------------------------------------------------------------------------

    # Prosta pętla pozwalająca tymczasowo przetestować działanie scenariusza.
    scene: SceneFrame = game.scene
    while len(scene.options):
        options = list()
        print(scene.title, scene.describe, '', sep='\n')
        i = 1
        for option in scene.options:
            options.append(option)
            print(i, ' > ', scene.options[option])
            i += 1
            pass
        data = input('>>')
        try:
            game.execute(options[int(data) - 1])
            pass
        except (IndexError, ValueError):
            print('error')
            pass
        scene = game.scene
        pass
    print(scene.title, scene.describe, '', sep='\n')
    game.close()
    pass
