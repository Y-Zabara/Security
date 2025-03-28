import rsa
import sympy

# Генерація слабких ключів для злому
(public_key, private_key) = rsa.newkeys(128)

# Повідомлення
message = "hello"
ciphertext = rsa.encrypt(message.encode(), public_key)

print(f"Ciphertext: {ciphertext.hex()}")
print(f"Public key (n): {public_key.n}")
print(f"Public key (e): {public_key.e}")


def rsa_attack(public_key, ciphertext):
    # Факторизація n
    n = public_key.n
    e = public_key.e
    factors = sympy.factorint(n)

    p, q = list(factors.keys())  # Отримуємо p і q

    # Обчислюємо закритий ключ
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)  # Обернений експонент

    # Розшифрування
    cipher_int = int.from_bytes(ciphertext, "big")  # Перетворення в число
    decrypted_int = pow(cipher_int, d, n)  # Дешифруємо
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, "big")

    
    return decrypted_bytes[-5:]  







def measure_rsa_performance(message_length):
    message = "A" * message_length  

    # Вимірюємо час шифрування
    start_time = time.time()
    ciphertext = rsa.encrypt(message.encode(), public_key)
    encrypt_time = time.time() - start_time

  
    start_time = time.time()
    decrypted_message = rsa.decrypt(ciphertext, private_key).decode()
    decrypt_time = time.time() - start_time

    return message_length, encrypt_time, decrypt_time


import time
import ecdsa
import os

def measure_signature_time(message_size):

    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    
    message = os.urandom(message_size)  
    

    start_time = time.time()
    signature = sk.sign(message)
    sign_time = time.time() - start_time
    

    start_time = time.time()
    is_valid = vk.verify(signature, message)
    verify_time = time.time() - start_time
    
    return sign_time, verify_time


message_sizes = range(50, 10000, 1000)
for size in message_sizes:
    sign_time, verify_time = measure_signature_time(size)
    print(f"Message size: {size} bytes | Sign time: {sign_time:.6f} s | Verify time: {verify_time:.6f} s")