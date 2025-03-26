class AffineCipherKeys:
    def __init__(self, key: str | None = None):
        self.keys = (7, 7)


class AffineCipher:
    def __init__(self, alphabet: str) -> None:
        self.alphabet: str = alphabet
        self.keys_storage: AffineCipherKeys = AffineCipherKeys()

    def encrypt(self, message):
        key_a, key_b = self.keys_storage.keys
        ciphertext = ""
        for symbol in message:
            if symbol in self.alphabet:
                sym_index = self.alphabet.find(symbol)
                ciphertext += self.alphabet[
                    (sym_index * key_a + key_b) % len(self.alphabet)
                ]
            else:
                ciphertext += symbol  # just append this symbol unencrypted
        return ciphertext

    def decrypt(self, message):
        key_a, key_b = self.keys_storage.keys

        plaintext = ""
        modInverseOfKeyA = self._find_mod_inverse(key_a, len(self.alphabet))
        for symbol in message:
            if symbol in self.alphabet:
                sym_index = self.alphabet.find(symbol)
                plaintext += self.alphabet[
                    (sym_index - key_b) * modInverseOfKeyA % len(self.alphabet)
                ]
            else:
                plaintext += symbol  # just append this symbol undecrypted
        return plaintext

    def brute_force_decrypt(self, message: str):
        result = ""
        old_keys = self.keys_storage.keys
        for key in range(2, len(self.alphabet)):
            self.keys_storage.keys = (key, key)
            plaintext = self.decrypt(message)
            result += f" key: {str((key,key))} {plaintext}\n"
        self.keys_storage.keys = old_keys
        return result


    def _gcd(
        self, a, b
    ):  # найбільший загальний дільник a, b за алгоритмом Евкліда (для шифрування)
        while a != 0:
            a, b = b % a, a
        return b

    def _find_mod_inverse(
        self, a, m
    ):  # модульне обертання за алгоритмом  Евкліда (для шифрування)
        if self._gcd(a, m) != 1:
            return None
        u1, u2, u3 = 1, 0, a
        v1, v2, v3 = 0, 1, m
        while v3 != 0:
            q = u3 // v3
            v1, v2, v3, u1, u2, u3 = (
                (u1 - q * v1),
                (u2 - q * v2),
                (u3 - q * v3),
                v1,
                v2,
                v3,
            )
        return u1 % m

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
    
    assert decrypted == test_message, "Помилка: Розшифроване повідомлення не збігається з оригіналом!"
    print("Усі тести пройдені успішно!")
    print(cipher.brute_force_decrypt(encrypted))
