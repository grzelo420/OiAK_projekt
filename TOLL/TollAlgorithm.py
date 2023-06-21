import numpy as np
import math
import random

from prime_numbers_generator import *


#   expected length - długość bloku danych w bitach (wielokrotność hex w bitach)
#   decimal_number  - liczba w sys dec w string
#   binary_string   - liczba w sys. bin w string
#   binary_array    - liczba w tablicy w sys. bin
#   shift_count     - ilość przesunięć binarnych
#   seqf_nr         - sekwencja jedynek (wielokrotnosc 8 bitow)

class TollAlgorithm:

    def __init__(self, hex_string):
        self.hex_string = hex_string

    @staticmethod
    def array_to_string(binary_array, data_type):
        # zamienia tablice binarna na string o danym typie
        if data_type == "hex":
            # Konwertuj na liczbę dziesiętną
            decimal_number = int("".join(binary_array), 2)
            # Konwertuj na liczbę szesnastkową
            hex_string = hex(decimal_number)[2:].upper()
            return hex_string
        elif data_type == "dec":
            # Konwertuj na liczbę dziesiętną
            decimal_number = int("".join(binary_array), 2)
            return str(decimal_number)
        elif data_type == "bin":
            # Zwróć łańcuch znaków bez konwersji
            return "".join(binary_array)
        else:
            return "Nieobsługiwany typ danych."

    @staticmethod
    def string_to_binary(data_string, data_type):
        if data_type == "hex":
            # Konwertuj szesnastkowy na dziesiętny
            decimal_number = int(data_string, 16)
            # Konwertuj dziesiętny na binarny
            binary_string = bin(decimal_number)[2:]
        elif data_type == "dec":
            # Konwertuj dziesiętny na binarny
            decimal_number = int(data_string)
            binary_string = bin(decimal_number)[2:]
        elif data_type == "bin":
            # Usuń niechciane znaki i sprawdź, czy pozostałe to tylko '0' i '1'
            binary_string = ''.join(filter(lambda c: c in ['0', '1'], data_string))
        else:
            return "Nieobsługiwany typ danych."

        # Zamień ciąg binarny na listę znaków
        binary_array = list(binary_string)

        return binary_array

    @staticmethod
    def hex_to_binary(hex_string):
        # zamienia stringa hexadecymalnego na tablice binarna
        expected_length = len(hex_string) * 4
        decimal_number = int(hex_string, 16)
        binary_string = bin(decimal_number)[2:]
        binary_string = binary_string.zfill(expected_length)
        binary_array = list(binary_string)

        return binary_array

    # TODO: metoda ma przyjmować dane typu liczba hex w string
    #   zwracac ma rownanie liniowe
    #   zamienic nazwy na angielskie

    @staticmethod
    def hex_to_coefficients(hex_num):
        equations = []
        j = -2
        k = 1
        # liczba_str = str(hex_num)     nie trzeba zamieniac na str() bo to juz jest string
        # print(liczba_str)
        decnumber = int(hex_num, 16)
        print('typ decnumber', type(decnumber))
        number_length = len(hex_num)

        for i in range(0, number_length, 2):
            byte = hex_num[i:i + 2]
            # print(byte)
            digit = int(byte, 16)
            # print(digit)
            if digit != 0:
                power = (number_length - i - 2) * 4
                if digit != 255:
                    equations.append(digit)
                    equations.append(power)
                    j += 2
                    k = 1
                else:
                    if j == -2:
                        equations.append('seqf' + str(8 * k))
                        equations.append(power)
                        j += 2
                    else:
                        if 'seqf' in str(equations[j]):
                            k += 1
                            equations[j] = 'seqf' + str(8 * k)
                            equations[j + 1] = power
                        else:
                            equations.append('seqf' + str(8 * k))
                            equations.append(power)
                            j += 2

        return equations

    @staticmethod
    def CSE(array):
        array_length = len(array)
        tabaddsub = []  # [i][1] tablica na dodaj/odejmij [i][2] tablica na shifts
        tabshift = []
        i = 0
        seq_counter = 0
        while i < len(array):
            if array[i] == 1:
                # jeżeli mamy jedynkę i potem zera to do tablicy wchodzi 1 i ilość przesunięć
                if i + 1 < len(array) and array[i + 1] == 0:
                    tabaddsub.append(1)
                    tabshift.append(array_length - i)
                    i += 1
                elif i + 1 < len(array) and array[i + 1] == 1:
                    tabaddsub.append(1)
                    tabshift.append(array_length - i + 1)  # + 1
                    while i + 1 < len(array) and array[i + 1] == 1:
                        i += 1
                    tabaddsub.append(-1)
                    tabshift.append(array_length - i)
                    i += 1
                elif i + 1 == len(array):  # Jeśli ostatnia pozycja to '1'
                    tabaddsub.append(1)
                    tabshift.append(0)
                    i += 1
            elif array[i] == 0:
                i += 1

        return tabshift, tabaddsub

    @staticmethod
    def printCSD(przesuniecia, dodajodejmij):

        for i in range(2 * len(przesuniecia) - 2):
            print("(", end="")
        print("", dodajodejmij[0], "<<", przesuniecia[0] - przesuniecia[1], end=" ) ")
        iterator = 1
        while iterator < len(przesuniecia) - 1:
            if iterator > 0:
                if dodajodejmij[iterator] == 1:
                    print("+", end="")
                else:
                    print("-", end="")
            if przesuniecia[iterator + 1] != 0:
                print("", 1, ") <<", przesuniecia[iterator] - przesuniecia[iterator + 1], end=" ) ")
                iterator += 1
            else:
                print("", 1, ") <<", przesuniecia[iterator] - przesuniecia[iterator + 1] - 1, end=" ) ")
                iterator += 1
        if dodajodejmij[iterator] == 1:
            print("+", end="")
        else:
            print("-", end="")
        if przesuniecia[len(przesuniecia) - 1] != 0:
            if (przesuniecia[len(przesuniecia) - 1] - 1) != 0:
                print("", 1, ") <<", przesuniecia[len(przesuniecia) - 1] - 1, end="")
            else:
                print("", 1, end="")
        else:
            print("", 1, end="")
        print()


TOLL = TollAlgorithm
print(12)
tabshift, tabaddsub = TOLL.CSE([0, 0, 0, 0, 1, 1, 0, 0])
TOLL.printCSD(tabshift, tabaddsub)
print(57)
tabshift, tabaddsub = TOLL.CSE([0, 0, 1, 1, 1, 0, 0, 1])
TOLL.printCSD(tabshift, tabaddsub)
print(164)
tabshift, tabaddsub = TOLL.CSE([1, 0, 1, 0, 0, 1, 0, 0])
TOLL.printCSD(tabshift, tabaddsub)
print(195)
tabshift, tabaddsub = TOLL.CSE([1, 1, 0, 0, 0, 0, 1, 1])
TOLL.printCSD(tabshift, tabaddsub)
print(228)
tabshift, tabaddsub = TOLL.CSE([1, 1, 1, 0, 0, 1, 0, 0])
TOLL.printCSD(tabshift, tabaddsub)


def common_subexpression(bin1, bin2):
    # Zapisujemy długość obu liczb
    len_bin1 = len(bin1)
    len_bin2 = len(bin2)

    # Zaczynamy od pustego najdłuższego wspólnego podwyrażenia
    max_subexpression = []

    # Przesuwamy bin1 w stosunku do bin2
    for i in range(-(len_bin1 - 1), len_bin2):
        subexpression = []
        # Porównujemy bity
        for j in range(len_bin2):
            if i + j < 0 or i + j >= len_bin1:
                continue
            if bin1[i + j] == bin2[j]:
                subexpression.append(bin2[j])
            else:
                if len(subexpression) > len(max_subexpression):
                    max_subexpression = list(subexpression)
                subexpression = []
        if len(subexpression) > len(max_subexpression):
            max_subexpression = list(subexpression)

        # Przerywamy pętlę jeśli nie jest możliwe znalezienie dłuższego podwyrażenia
        if len(max_subexpression) >= len_bin2 - i:
            break

    # Zwracamy wynik jako listę
    return max_subexpression


def coefficients(tablica):
    # Utworzenie pustego zbioru
    C = set()

    # Przechodzenie przez wszystkie elementy w tablicy
    for element in tablica:
        # Dodanie elementu do zbioru (jeżeli element już jest w zbiorze, to nie zostanie dodany ponownie)
        C.add(element)

    # Zwrócenie listy unikalnych elementów
    return list(C)


# Testujemy funkcję
# rownania = ['a', 'b', 'a', 'c', 'b', 'd', 'e', 'f', 'f']
# print(coefficients(rownania))

# Testujemy funkcję
# print(joint_subexpression(['1', '0', '1', '1', '1', '0', '1'], ['1', '1', '0', '1', '1']))

# hex_number = '0000'
# binary_number = hex_to_binary(hex_number)
# print(binary_number)

"""""
        uproszczona procedura testu
"""""

liczba0 = 31910012456
liczba1 = 44309669216255
liczba2 = 1095546312524

# liczba_hex = "%0.14X" % liczba1  # string

# tablica_bin = TOLL.string_to_binary(liczba_hex, "hex")  # list
#
# liczba_bin = TOLL.array_to_string(tablica_bin, "bin")  # string
# liczba_dec = TOLL.array_to_string(tablica_bin, "dec")  # string
# equation = TOLL.hex_to_coefficients(liczba_hex)
# print('=========================================')
# print('dlugosc liczby w bitach:', len(liczba_bin))
# print()
# print('liczba hex:', liczba_hex)
# print('typ struktury:', type(liczba_hex))
# print()
# print('liczba dec:', liczba_dec)
# print('typ struktury:', type(liczba_dec))
# print()
# print('liczba dec:', liczba_bin)
# print('typ struktury:', type(liczba_bin))
# print()
# print('tablica binarna do operacji shift:', tablica_bin)
# print('typ struktury:', type(tablica_bin))
# print()
# print('rownanie:', equation)
# print('typ struktury:', type(equation))
# print()
# print('2, 4 i 6 blok liczby w dec:')
# print(equation[1], equation[3], equation[5])


# rownania = hex_na_rownania(liczba_hex)
# print(str(liczba_hex))
# TollAlgorithnm.rownania = TollAlgorithnm.hex_to_coefficients(liczba_hex)
# print(TollAlgorithnm.rownania)

# liczba_hex = "%0.14X" % liczba2
# print(str(liczba_hex))
# equations = TollAlgorithnm.hex_to_coefficients(liczba_hex)
# print(equations)

# print(rownania[3])
# print(rownania[4])
# liczba_str = str(liczba_hex)
# print(liczba_str)
