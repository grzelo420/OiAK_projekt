import numpy as np
import math
import random

from prime_numbers_generator import *


#   expected length - długość bloku danych w bitach (wielokrotność hex w bitach)
#   decimal_number  - liczba w sys dec w string
#   binary_string   - liczba w sys. bin w string
#   binary_array    - liczba w tablicy w sys. bin
#   shift_count     - ilość przesunięć binarnych

class TollAlgorithnm:

    def __init__(self, hex_string):
        self.hex_string = hex_string

    @staticmethod
    def hex_to_binary(hex_string):
        # zamienia stringa hexadecymalnego na tablice binarna
        expected_length = len(hex_string) * 4
        decimal_number = int(hex_string, 16)
        binary_string = bin(decimal_number)[2:]
        binary_string = binary_string.zfill(expected_length)
        binary_array = list(binary_string)

        return binary_array

    @staticmethod
    def shift_left(binary_array, shift_count):
        # przesuwa tablice dwujkowa o nadana ilosc bitow w lewo
        shifted_array = binary_array[shift_count:] + ['0'] * shift_count

        return shifted_array

    # TODO: metoda ma przyjmować dane typu liczba hex w string
    #   zwracac ma rownanie liniowe
    #   zamienic nazwy na angielskie

    @staticmethod
    def hex_to_coefficients(hex_num):
        liczba_str = str(hex_num)
        liczba_dec = int(liczba_str, 16)
        liczba_dlugosc = len(liczba_str)
        equations = []
        j = -2
        k = 1
        for i in range(0, liczba_dlugosc, 2):
            bajt = liczba_str[i:i + 2]
            cyfra = int(bajt, 16)
            if cyfra != 0:
                potega = (liczba_dlugosc - i - 2) * 4
                if cyfra != 255:
                    rownania.append(cyfra)
                    rownania.append(potega)
                    j += 2
                    k = 1
                else:
                    if j == -2:
                        rownania.append('seqf' + str(8 * k))
                        rownania.append(potega)
                        j += 2
                    else:
                        if 'seqf' in str(rownania[j]):
                            k += 1
                            rownania[j] = 'seqf' + str(8 * k)
                            rownania[j + 1] = potega
                        else:
                            rownania.append('seqf' + str(8 * k))
                            rownania.append(potega)
                            j += 2

        return rownania

    # hex_number = '0000'
    # binary_number = hex_to_binary(hex_number)
    # print(binary_number)


"""""
        uproszczona procedura testu
"""""

liczba0 = 31910012456
liczba1 = 44309669216255
liczba2 = 1095546312524

# rownania = hex_na_rownania(liczba_hex)
liczba_hex = "%0.14X" % liczba1
print(str(liczba_hex))
rownania = TollAlgorithnm.hex_to_coefficients(liczba_hex)
print(rownania)

liczba_hex = "%0.14X" % liczba2
print(str(liczba_hex))
rownania = TollAlgorithnm.hex_to_coefficients(liczba_hex)
print(rownania)

# print(rownania[3])
# print(rownania[4])
# liczba_str = str(liczba_hex)
# print(liczba_str)
