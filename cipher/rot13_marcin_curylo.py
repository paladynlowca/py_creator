from random import Random
from typing import Callable, List


class MenuError(Exception):
    pass


# Uniwersala klasa menu przygotowana z myślą o przyszłych implementacjach
class Menu:
    class MenuOption:
        def __init__(self, text: str, key: str, action: Callable[[], None]):
            self._text = text
            self._key = key.upper()
            self._action = action
            pass

        @property
        def action(self):
            return self._action

        @property
        def key(self):
            return self._key

        def __str__(self):
            return f'{self._key} - {self._text}'

        def __eq__(self, other: str):
            if self._key == other.upper():
                return True
            return False

        pass

    def __init__(self):
        self._options: List[Menu.MenuOption] = list()
        pass

    @property
    def keys(self):
        keys = list()
        keys.append('X')
        for option in self._options:
            keys.append(option.key)
        return keys

    def add_option(self, text: str, key: str, action: Callable[[], None]):
        if key.upper() not in self.keys:
            self._options.append(self.MenuOption(text, key, action))
            return True
        return False

    def print(self):
        print()
        for option in self._options:
            print(option)
            pass
        print('X - Wyjście')
        pass

    def choose(self):
        print('Dokonaj wyboru')
        choice = input('>>')
        if choice.upper() == 'X':
            print('Do widzenia.\n<ENTER żeby zakończyć>')
            input()
            exit(0)
        for option in self._options:
            if option == choice:
                return option.action
            pass
        print('Błędny wybór.')
        return False

    def run(self):
        while True:
            self.print()
            action = self.choose()
            if action:
                try:
                    action()
                    pass
                except MenuError as exception:
                    print(f'Nastapił błąd przetwazania polecenia z wiadomością: {exception}')
                pass
            pass
        pass

    pass


# Pobieranie tekstu do za/rozszyfrowania od użytkownika
def get_input(reverse: bool = False):
    word = 'zaszyfrowania' if not reverse else 'odszyfrowania'
    # pobieranie tekstu do zaszyfrowania
    print(f'Wprowadź ciąg do {word}:')
    return input('>>')


def encode(reverse: bool = False):
    # Pobranie tekstu od użytkownika i przygotowanie tablicy z szyfrem
    text = get_input(reverse)
    # Zaszyfrowanie kolejnych znaków
    output = ''
    move = 0
    # Dla każdego znaku
    for char in [ord(ch) for ch in text]:
        # Przesuń małe litery o 13 pozycji
        if 97 <= char <= 122:
            output += chr((char - 97 + 13) % 26 + 97)
            pass
        # Przesuń wielkie litery o 13 pozycji
        elif 65 <= char <= 90:
            output += chr((char - 65 + 13) % 26 + 65)
            pass
        # Przepisz rtesztę znaków
        else:
            output += chr(char)
            pass
        pass
    # Wypisywanie wyniku
    word = 'Zaszyfrowana' if not reverse else 'Odszyfrowana'
    print(f'{word} wiadomość to:')
    print(output)
    pass


def decode():
    encode(True)
    pass


if __name__ == '__main__':
    # Inicjowanie menu i dodawanie opcji szyfrowania oraz rozszyfrowania
    menu = Menu()
    menu.add_option('Szyfowanie ROT-13', '1', encode)
    menu.add_option('Deszyfowanie ROT-13', '2', decode)
    # Uruchomienie pętli głównej programu
    menu.run()
    pass
