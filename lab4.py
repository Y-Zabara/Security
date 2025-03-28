from Cipher.Caesar import CaesarCipher


if __name__ == "__main__":
    # Define the alphabet and create an instance of CaesarCipher
    alphabet = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦШЩЬЮЯабвгдеєжзиіїйклмнопрстуфхцшщьюя"
    key = 3
    cipher = CaesarCipher(alphabet, key)

    # Original message
    text = "Привіт світ!"
    
    # Encrypt and decrypt the message
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)

    # Print results
    print(f"Alphabet: {alphabet}")
    print(f"Key: {key}")
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

    # Attempt to brute-force decrypt the message and measure execution time
    execution_time, hacker_result = cipher.brute_force_decrypt(encrypted)
    print(f"Hacker attempt (brute force):\n{hacker_result}")
    print(f"Execution time: {execution_time:.6f} seconds")

