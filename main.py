from element import Code
from game import Game
from constans import *

if __name__ == '__main__':
    game = Game()
    # Tworzenie wszystkich elementów potrzebnych do działania scenariusza.
    scene1, scene2, scene3, scene4 = Code('s1', SCENE), Code('s2', SCENE), Code('s3', SCENE), Code('s4', SCENE)
    game.build_scene(scene1.code, _title_='Korytarz', _description_='Jesteś w dość krótkim korytarzu.')
    game.build_scene(scene2.code, _title_='Ganek', _description_='To zdecydowanie jest ganek, możesz wyjść na zewnątrz.')
    game.build_scene(scene3.code, _title_='Ulica', _description_='Wyszedłeś na ulicę wprost pod nadjeżdzający walec drogowy. Umarłeś.')
    game.build_scene(scene4.code, _title_='Kuchnia.', _description_='Wszedłeś do kuchni. Nie ma tu nic ciekawego.')

    trigger1, trigger2, trigger3, trigger4 = Code('trigger1', TRIGGER), Code('trigger2', TRIGGER), Code('trigger3', TRIGGER), Code('trigger4', TRIGGER)
    game.create_element(trigger1)
    game.create_element(trigger2)
    game.create_element(trigger3)
    game.create_element(trigger4)

    option1, option2, option3, option4 = Code('option1', OPTION), Code('option2', OPTION), Code('option3', OPTION), Code('option4', OPTION)
    game.build_option(option1.code, 'Wejdź w drzwi po prawej.')
    game.build_option(option2.code, 'Wejdź w drzwi po lewej.')
    game.build_option(option3.code, 'Wróć na korytarz.')
    game.build_option(option4.code, 'Wyjdź na zewnątrz.')

    trigger21, trigger22, trigger23, trigger24 = Code('trigger21', TRIGGER), Code('trigger22', TRIGGER), Code('trigger23', TRIGGER), Code('trigger24', TRIGGER)
    game.create_element(trigger21)
    game.create_element(trigger22)
    game.create_element(trigger23)
    game.create_element(trigger24)

    action1, action2, action3, action4 = Code('target1', ACTION), Code('target2', ACTION), Code('target3', ACTION), Code('target4', ACTION)
    game.create_element(Code(action1.code, TARGET_ACTION))
    game.create_element(Code(action2.code, TARGET_ACTION))
    game.create_element(Code(action3.code, TARGET_ACTION))
    game.create_element(Code(action4.code, TARGET_ACTION))

    # ----------------------------------------------------------------------------

    # Korytarz -> ganek
    game.add_relation(scene1, trigger1)
    game.add_relation(trigger1, option1)
    game.add_relation(option1, trigger21)
    game.add_relation(trigger21, action1)
    game.add_relation(action1, scene2)

    # Korytarz -> kuchnia
    game.add_relation(scene1, trigger2)
    game.add_relation(trigger2, option2)
    game.add_relation(option2, trigger22)
    game.add_relation(trigger22, action2)
    game.add_relation(action2, scene4)

    # Ganek -> korytarz
    game.add_relation(scene2, trigger3)
    game.add_relation(trigger3, option3)
    game.add_relation(option3, trigger23)
    game.add_relation(trigger23, action3)
    game.add_relation(action3, scene1)

    # kuchnia -> Korytarz
    game.add_relation(scene4, trigger3)
    game.add_relation(trigger3, option3)

    # Ganek -> Ulica
    game.add_relation(scene2, trigger4)
    game.add_relation(trigger4, option4)
    game.add_relation(option4, trigger24)
    game.add_relation(trigger24, action4)
    game.add_relation(action4, scene3)

    # Prosta pętla pozwalająca tymczasowo przetestować działanie scenariusza.
    game.change_scene(scene1)
    while game.options:
        print(game.scene[0], game.scene[1], '', sep='\n')
        i = 1
        for option in game.options:
            print(i, ' > ', option[0])
            i += 1
            pass
        data = input('>>')
        try:
            game.execute(game.options[int(data) - 1][1])
            pass
        except (IndexError, ValueError):
            print('error')
            pass
        pass
    print(game.scene[0], game.scene[1], sep='\n')
    game.close()
    pass
