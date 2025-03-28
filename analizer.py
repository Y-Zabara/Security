import time
from repositories import RegularFileRepo
from Cipher.Caesar import CaesarCipher
from Cipher.AffineCipher import AffineCipher
from Cipher.RC4 import RC4
from alphabets import ENGLISH_ALPHABET

def encrypt_time(Cipher, message: str):
    start_time = time.perf_counter()  # Start measuring time
    encrypted = Cipher.encrypt(message)
    end_time = time.perf_counter()  # End measuring time
    time1 =  round(end_time - start_time, 4)

    start_time = time.perf_counter()  # Start measuring time
    Cipher.decrypt(encrypted)
    end_time = time.perf_counter()  # End measuring time
    time2 = round(end_time - start_time, 4)

    start_time = time.perf_counter()  # Start measuring time
    Cipher.brute_force_decrypt(encrypted)
    end_time = time.perf_counter()  # End measuring time
    time3 = round(end_time - start_time, 4)
    return time1, time2, time3

def analize(Cipher, message_len_range) -> dict:
    file = RegularFileRepo("shakespeare.txt")
    result = {}
    for i in range(*message_len_range):
        message = file.get_n_chars(i)
        times = encrypt_time(Cipher, message)
        result[i] = {"encrypt": str(times[0]),
                     "decrypt": str(times[1]),
                     "brute_force_attack": str(times[2])}
    return result

if __name__ == "__main__":
    cipher = CaesarCipher(ENGLISH_ALPHABET, 4)
    cipher = AffineCipher(ENGLISH_ALPHABET)
    cipher = RC4("keyy")
    file = RegularFileRepo("shakespeare.txt")

    print(analize(cipher, (50, 101, 50)))
