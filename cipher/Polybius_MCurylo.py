from typing import Callable, List


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
                action()
                pass
            pass
        pass

    pass


# Tablice ze znakami i kodami służące do wygenerowania tabeli kodowej
chars_letters = ['A', 'B', 'C', 'D', 'E',
                 'F', 'G', 'H', 'I', 'K',
                 'L', 'M', 'N', 'O', 'P',
                 'Q', 'R', 'S', 'T', 'U',
                 'V', 'W', 'X', 'Y', 'Z']

chars_numbers = ['11', '12', '13', '14', '15',
                 '21', '22', '23', '24', '25',
                 '31', '32', '33', '34', '35',
                 '41', '42', '43', '44', '45',
                 '51', '52', '53', '54', '55']


# Pobieranie tekstu do za/rozszyfrowania od użytkownika
def get_input(reverse: bool = False):
    word = 'zaszyfrowania' if not reverse else 'odszyfrowania'
    # pobieranie tekstu do zaszyfrowania
    print(f'Wprowadź ciąg do {word}:')
    return input('>>').upper()


# Pobieranie hasła szyfrogramu
def get_password():
    print('Podaj hasło')
    return input('>>').upper()


# Przygotowanie tablicy kodującej
def prepare_encode_table(password: str = ''):
    # Tworzenie tablicy wyjściowej i iteratora z którego pobierane będą kolejne wartości szyfru
    output = dict()
    iterator = iter(chars_numbers)
    # Iterowanie po literach hasła
    for char in password.upper():
        if char not in output and char in chars_letters:  # Sprawdzenie, czy znak jest literą i nie ma go w tablicy
            output[char] = next(iterator)  # Przypisanie do każdej litery kolejnej wartości szyfru
            pass
        pass
    # Dodanie do tablicy liter niewystępujących w haśle
    for char in chars_letters:
        if char not in output:  # Sprawdzenie, czy znaku nie ma w tablicy
            output[char] = next(iterator)  # Przypisanie do każdej litery kolejnej wartości szyfru
    return output
    pass


def prepare_decode_table(password: str = ''):
    output = dict()
    iterator = iter(chars_numbers)
    for char in password.upper():
        if char not in output.values() and char in chars_letters:  # Sprawdzenie, czy znak jest literą i nie ma go w tablicy
            output[next(iterator)] = char  # Przypisanie do kolejnej wartości szyfru litery z hasła
            pass
        pass
    for char in chars_letters:
        if char not in output.values():  # Sprawdzenie, czy znaku nie ma w tablicy
            output[next(iterator)] = char  # Przypisanie do kolejnej wartości szyfru litery
    return output
    pass


def encode(password: str = ''):
    # Pobranie tekstu od użytkownika i przygotowanie tablicy z szyfrem
    text = get_input().replace('J', 'I')
    table = prepare_encode_table(password)
    # Zaszyfrowanie kolejnych znaków
    output = ''
    for char in text:
        if char in table:
            output += table[char]
            pass
        pass
    # Wypisywanie wyniku
    print('Zaszyfrowana wiadomość to:')
    print(output)
    pass


def encode_clear():
    # Szyfrowanie bez hasła
    encode()
    pass


def encode_password():
    # Szyfrowanie z hasłem
    encode(get_password())
    pass


def decode(password: str = ''):
    # Pobranie tekstu od użytkownika i przygotowanie tablicy z szyfrem
    text = get_input(True)
    table = prepare_decode_table(password)
    output = ''
    # Rozszyfrowanie kolejnych znaków
    for char in [text[i:i + 2] for i in range(0, len(text), 2)]:
        if char in table:
            output += table[char]
            pass
        pass
    # Wypisywanie wyniku
    print('Rozszyfrowana wiadomość to:')
    print(output)
    pass


def decode_clear():
    # Rozszyfrowanie bez hasła
    decode()
    pass


def decode_password():
    # Rozszyfrowanie z hasłem
    decode(get_password())
    pass


if __name__ == '__main__':
    # Inicjowanie menu i dodawanie opcji szyfrowania oraz rozszyfrowania
    menu = Menu()
    menu.add_option('Szyfowanie Polibiusza', '1', encode)
    menu.add_option('Szyfowanie Polibiusza z hasłem', '2', encode_password)
    menu.add_option('Deszyfowanie Polibiusza', '3', decode)
    menu.add_option('Deszyfowanie Polibiusza z hasłem', '4', decode_password)
    # Uruchomienie pętli głównej programu
    menu.run()
    pass
