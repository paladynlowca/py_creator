from constans import *
from data_frame import SceneFrame
from engine.element import Code
from engine.game import Game
from xml_handler.xml_loader import XMLLoader

if __name__ == '__main__':
    game = Game()
    # Tworzenie wszystkich elementów potrzebnych do działania scenariusza.
    scene_hall, scene_entry = Code('hall', SCENE), Code('entry', SCENE)
    scene_street, scene_kitchen = Code('street', SCENE), Code('kitchen', SCENE)
    game.build_element(scene_hall, _title_='Korytarz', _description_='Jesteś w dość krótkim korytarzu.')
    game.build_element(scene_entry, _title_='Ganek',
                       _description_='To zdecydowanie jest ganek, możesz wyjść na zewnątrz.')
    game.build_element(scene_street, _title_='Ulica',
                       _description_='Wyszedłeś na ulicę wprost pod nadjeżdzający walec drogowy. Umarłeś.')
    game.build_element(scene_kitchen, _title_='Kuchnia.', _description_='Wszedłeś do kuchni. Nie ma tu nic ciekawego.')

    option_to_entry, option_to_kitchen = Code('to_entry', OPTION), Code('to_kitchen', OPTION),
    option_to_hall, option_to_street = Code('to_hall', OPTION), Code('to_street', OPTION)
    game.build_element(option_to_entry, _text_='Wejdź w drzwi po prawej.')
    game.build_element(option_to_kitchen, _text_='Wejdź w drzwi po lewej.')
    game.build_element(option_to_hall, _text_='Wróć na korytarz.')
    game.build_element(option_to_street, _text_='Wyjdź na zewnątrz.')

    action_go_entry, action_go_kitchen = Code('go_entry', ACTION), Code('go_kitchen', ACTION),
    action_go_hall, action_go_street = Code('go_hall', ACTION), Code('go_street', ACTION)
    game.build_element(action_go_entry, _precise_type_=TARGET_ACTION)
    game.build_element(action_go_kitchen, _precise_type_=TARGET_ACTION)
    game.build_element(action_go_hall, _precise_type_=TARGET_ACTION, _time_increase_=5)
    game.build_element(action_go_street, _precise_type_=TARGET_ACTION)

    action_change_bool = Code('change_bool', ACTION)
    game.build_element(action_change_bool, _precise_type_=VARIABLE_ACTION, _change_type_=VARIABLE_INVERSE)

    var_int, var_bool = Code('var_int_1', VARIABLE), Code('var_bool_1', VARIABLE)
    game.build_element(var_int, _precise_type_=INT_VARIABLE)
    game.build_element(var_bool, _precise_type_=BOOL_VARIABLE)

    con_int, con_bool = Code('con_int_1', CONDITION), Code('con_bool_1', CONDITION)
    con_multi = Code('con_multi_1', CONDITION)
    con_sub1, con_sub2 = Code('con_sub_1', CONDITION), Code('con_sub_2', CONDITION)
    game.build_element(con_int, _precise_type_=INT_CONDITION, _test_type_=MORE, _expected_value_=2)
    game.build_element(con_bool, _precise_type_=BOOL_CONDITION, _test_type_=EQUAL, _expected_value_=True)
    game.build_element(con_multi, _precise_type_=MULTI_CONDITION, _test_type_=MULTI_AND, _expected_value_=True)
    game.build_element(con_sub1, _precise_type_=INT_CONDITION, _test_type_=EQUAL, _expected_value_=3)
    game.build_element(con_sub2, _precise_type_=BOOL_CONDITION, _test_type_=EQUAL, _expected_value_=True)
    a = game[var_int]
    a.value = 3
    a = game[var_bool]
    a.value = False

    # ------------------------------------------------------------------------------------------------------------------

    # Dodawanie relacji pomiędzy obiektami, w komentarzach są kierunki przejść pomiędzy scenami.
    # Korytarz -> ganek
    game.add_relation(scene_hall, option_to_entry)
    game.add_relation(option_to_entry, action_go_entry)
    game.add_relation(option_to_entry, con_multi)
    game.add_relation(action_go_entry, scene_entry)

    # Korytarz -> kuchnia
    game.add_relation(scene_hall, option_to_kitchen)
    game.add_relation(option_to_kitchen, action_go_kitchen)
    # game.add_relation(option_to_kitchen, con_int)
    game.add_relation(option_to_kitchen, action_change_bool)
    game.add_relation(action_go_kitchen, scene_kitchen)

    # Ganek -> korytarz
    game.add_relation(scene_entry, option_to_hall)
    game.add_relation(option_to_hall, action_go_hall)
    game.add_relation(action_go_hall, scene_hall)

    # kuchnia -> Korytarz (podpięcie porzednio zbudowanej opcji)
    game.add_relation(scene_kitchen, option_to_hall)

    # Ganek -> Ulica
    game.add_relation(scene_entry, option_to_street)
    game.add_relation(option_to_street, action_go_street)
    game.add_relation(action_go_street, scene_street)

    # zmienne

    game.add_relation(con_int, var_int)
    game.add_relation(con_bool, var_bool)
    game.add_relation(action_change_bool, var_bool)

    game.add_relation(con_multi, con_sub1)
    game.add_relation(con_multi, con_sub2)
    game.add_relation(con_sub1, var_int)
    game.add_relation(con_sub2, var_bool)

    game.change_scene(scene_hall)

    file = XMLLoader(game, 'test3')
    exit(0)
    # ------------------------------------------------------------------------------------------------------------------

    # Prosta pętla pozwalająca tymczasowo przetestować działanie scenariusza.
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
