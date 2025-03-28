from Cipher.RC4 import RC4
from repositories import RegularFileRepo

if __name__ == "__main__":
    key = "key"
    cipher = RC4(key)
    
    # Тестові дані
    test_message = "Hello123"
    encrypted = cipher.encrypt(test_message)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Оригінал: {test_message}")
    print(f"Зашифроване: {encrypted}")
    print(f"Розшифроване: {decrypted}")

    print("\n Читання з файлу")
    test_message = RegularFileRepo("shakespeare.txt").get_n_chars(100)
    encrypted = cipher.encrypt(test_message)
    decrypted = cipher.decrypt(encrypted)
    
    print(f"Оригінал: {test_message}")
    print(f"Зашифроване: {encrypted}")
    print(f"Розшифроване: {decrypted}")