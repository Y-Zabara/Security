from Cipher.AffineCipher import AffineCipher


if __name__ == "__main__":
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    cipher = AffineCipher(alphabet)
    
    # Тестові дані
    test_message = "Hello123"
    encrypted = cipher.encrypt(test_message)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Оригінал: {test_message}")
    print(f"Зашифроване: {encrypted}")
    print(f"Розшифроване: {decrypted}")
    print(cipher.brute_force_decrypt(encrypted))