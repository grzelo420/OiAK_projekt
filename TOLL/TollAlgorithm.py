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
        #liczba_str = str(hex_num)     nie trzeba zamieniac na str() bo to juz jest string
        #print(liczba_str)
        decnumber = int(hex_num, 16)
        numberlength = len(hex_num)

        for i in range(0, numberlength, 2):
            byte = hex_num[i:i + 2]
            # print(byte)
            digit = int(byte, 16)
            #print(digit)
            if digit != 0:
                power = (numberlength - i - 2) * 4
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
    def shift_left(array, shift_count):

        shifted_array = array[shift_count:] + ['0'] * shift_count

        return shifted_array

    # hex_number = '0000'
    # binary_number = hex_to_binary(hex_number)
    # print(binary_number)


"""""
        uproszczona procedura testu
"""""

liczba0 = 31910012456
liczba1 = 44309669216255
liczba2 = 1095546312524

TOLL = TollAlgorithm

liczba_hex = "%0.14X" % liczba1
liczba_bin = TOLL.array_to_string(TOLL.string_to_binary(liczba_hex, "hex"), "bin")
liczba_dec = TOLL.array_to_string(TOLL.string_to_binary(liczba_hex, "hex"), "dec")

print(type(TOLL.string_to_binary(liczba_hex, "hex")))

print('hex:', liczba_hex, type(liczba_hex))
print('dec:', liczba_dec)
print('dec:', liczba_bin)
print('ile bitow:', len(liczba_bin))
print('rownanie:', TOLL.hex_to_coefficients(liczba_hex))

# rownania = hex_na_rownania(liczba_hex)
# print(str(liczba_hex))
#TollAlgorithnm.rownania = TollAlgorithnm.hex_to_coefficients(liczba_hex)
# print(TollAlgorithnm.rownania)

#liczba_hex = "%0.14X" % liczba2
# print(str(liczba_hex))
#equations = TollAlgorithnm.hex_to_coefficients(liczba_hex)
# print(equations)

# print(rownania[3])
# print(rownania[4])
# liczba_str = str(liczba_hex)
# print(liczba_str)
