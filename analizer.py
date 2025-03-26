import time
from repositories import RegularFileRepo
from Caesar import CaesarCipher
from alphabets import ENGLISH_ALPHABET

def encrypt_time(Cipher, message: str):
    start_time = time.perf_counter()  # Start measuring time
    Cipher.encrypt(message)
    end_time = time.perf_counter()  # End measuring time
    return round(end_time - start_time, 4)

def decrypt_time(Cipher, message: str):
    start_time = time.perf_counter()  # Start measuring time
    Cipher.decrypt(message)
    end_time = time.perf_counter()  # End measuring time
    return round(end_time - start_time, 4)

def brute_force_decrypt_time(Cipher, message: str):
    start_time = time.perf_counter()  # Start measuring time
    Cipher.brute_force_decrypt(message)
    end_time = time.perf_counter()  # End measuring time
    return round(end_time - start_time, 4)

def analize(Cipher, message_len_range) -> dict:
    file = RegularFileRepo("shakespeare.txt")
    result = {}
    for i in range(*message_len_range):
        message = file.get_n_chars(i)
        result[i] = {"encrypt": str(encrypt_time(Cipher, message)),
                     "decrypt": str(decrypt_time(Cipher, message)),
                     "brute_force_attack": str(brute_force_decrypt_time(Cipher, message))}
    return result

if __name__ == "__main__":
    cipher = CaesarCipher(ENGLISH_ALPHABET, 4)
    file = RegularFileRepo("shakespeare.txt")
    n = 100000
    print(f"""{
    encrypt_time(cipher, file.get_n_chars(n)),
    brute_force_decrypt_time(cipher, file.get_n_chars(n)),
    decrypt_time(cipher, file.get_n_chars(n))}""")

    print(analize(cipher, (50, 2000, 400)))
