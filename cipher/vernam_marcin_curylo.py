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
        if key.isalnum() and key.upper() not in self.keys:
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


# Pobieranie tekstu do zaszyfrowania od użytkownika
def get_input(reverse: bool = False):
    word = 'zaszyfrowania' if not reverse else 'odszyfrowania'
    # pobieranie tekstu do zaszyfrowania
    print(f'Wprowadź ciąg do {word}:')
    return input('>>')


# Pobieranie zaszyfrowanego ciągu od użytkownika
def get_crypto(req: int = 0):
    print(f'Wprowadź szyfrogram:')
    text = input('>>')
    # Sprawdzenie, czy jest to liczba szesnastkowa oraz czy ma parzystą ilość znaków (czy jest ciągiem liczb 00 - FF).
    if len([1 for char in text if char not in '1234567890abcdef']) or len(text) % 2:
        if req >= 16:
            raise MenuError('Zbyt wiele błędnych szyfogramów.')
        print('Błędny szyfrogram, podaj poprawny.')
        text = get_crypto(req=req + 1)
        pass
    return text


# Pobieranie hasła od użytkownika
def get_password(data: str, req: int = 0):
    print('Wprowadź hasło do szyfrogramu:')
    password = input('>>')
    # Sprawdzenie, czy jest to liczba szesnastkowa o długości równej długości szyfrogramu.
    if len([1 for char in password if char not in '1234567890abcdef']) or len(password) != len(data):
        if req >= 16:
            raise MenuError('Zbyt wiele błędnych haseł.')
        print('Błędne hasło, podaj poprawne.')
        password = get_password(data, req=req + 1)
        pass
    return password


def encode():
    # Pobranie tekstu i utworzenie z niego tablicy bajtów.
    text = get_input()
    byte_text = bytearray(text, encoding='cp1250', errors='replace')

    # Wygenerowanie tablicy hasła z pseudolosowymi wartościami 0-255.
    random = Random()
    byte_pass = bytearray([random.randint(0, 255) for i in range(len(byte_text))])
    # Operacja XOR na każdej parze bajtów tekstu i hasła.
    byte_crypto = bytearray(byte_text ^ byte_pass for (byte_text, byte_pass) in zip(byte_text, byte_pass))
    # Wypisanie hasła i szyfrogramu.
    print('Hasło do szyfrogramu:')
    print(byte_pass.hex())
    print('Szyfrogram:')
    print(byte_crypto.hex())
    pass


def decode():
    # Pobranie od użytkownika szyfrogramu i hasła, oraz przetworzenie ich do postaci tablicy bajtów.
    text = get_crypto()
    byte_pass = bytearray.fromhex(get_password(text))
    byte_crypto = bytearray.fromhex(text)
    # Operacja XOR na każdej parze bajtów szyfrogramu i hasła.
    byte_crypto = bytearray(byte_text ^ byte_pass for (byte_text, byte_pass) in zip(byte_crypto, byte_pass))
    # Wypisanie rozszyfrowanej wiadomości.
    print(byte_crypto.decode('cp1250', errors='replace'))
    pass


if __name__ == '__main__':

    menu = Menu()
    menu.add_option('Szyfrowanie Baudota.', '1', encode)
    menu.add_option('Deszyfrowanie Baudota.', '2', decode)
    menu.run()
    pass
