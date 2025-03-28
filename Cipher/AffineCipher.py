from typing import Optional


class AffineCipherKeys:
    """
    A class to store keys for the Affine Cipher.

    Attributes:
        keys (tuple[int, int]): A tuple containing the affine cipher keys (key_a, key_b).
    """

    def __init__(self, key: Optional[str] = None):
        """
        Initializes the key storage with default or provided values.

        Args:
            key (Optional[str]): Placeholder for a future key input method (currently unused).
        """
        self.keys = (7, 7)  # Default keys


class AffineCipher:
    """
    Implementation of the Affine Cipher encryption algorithm.

    Attributes:
        alphabet (str): The alphabet used for encryption and decryption.
        keys_storage (AffineCipherKeys): Storage for encryption keys.
    """

    def __init__(self, alphabet: str) -> None:
        """
        Initializes the Affine Cipher with a given alphabet.

        Args:
            alphabet (str): The character set used for encryption and decryption.
        """
        self.alphabet: str = alphabet
        self.keys_storage: AffineCipherKeys = AffineCipherKeys()

    def encrypt(self, message: str) -> str:
        """
        Encrypts a message using the Affine Cipher.

        Args:
            message (str): The plaintext message to encrypt.

        Returns:
            str: The encrypted ciphertext.
        """
        key_a, key_b = self.keys_storage.keys
        ciphertext = ""
        for symbol in message:
            if symbol in self.alphabet:
                sym_index = self.alphabet.find(symbol)
                ciphertext += self.alphabet[
                    (sym_index * key_a + key_b) % len(self.alphabet)
                ]
            else:
                ciphertext += symbol  # Append unencrypted symbol
        return ciphertext

    def decrypt(self, message: str) -> str:
        """
        Decrypts a message using the Affine Cipher.

        Args:
            message (str): The ciphertext to decrypt.

        Returns:
            str: The decrypted plaintext message.
        """
        key_a, key_b = self.keys_storage.keys

        plaintext = ""
        mod_inverse_of_key_a = self._find_mod_inverse(key_a, len(self.alphabet))
        if mod_inverse_of_key_a is None:
            raise ValueError("Invalid key, no modular inverse found.")

        for symbol in message:
            if symbol in self.alphabet:
                sym_index = self.alphabet.find(symbol)
                plaintext += self.alphabet[
                    (sym_index - key_b) * mod_inverse_of_key_a % len(self.alphabet)
                ]
            else:
                plaintext += symbol  # Append undecrypted symbol
        return plaintext

    def brute_force_decrypt(self, message: str) -> str:
        """
        Attempts to decrypt a message by trying all possible keys.

        Args:
            message (str): The ciphertext to brute-force.

        Returns:
            str: A formatted string with possible decryptions for each key.
        """
        result = ""
        old_keys = self.keys_storage.keys
        for key in range(2, 2000):
            self.keys_storage.keys = (key, key)
            try:
                plaintext = self.decrypt(message)
                result += f" key: {str((key, key))} {plaintext}\n"
            except Exception:
                continue
        self.keys_storage.keys = old_keys
        return result

    def _gcd(self, a: int, b: int) -> int:
        """
        Computes the greatest common divisor (GCD) using Euclidean algorithm.

        Args:
            a (int): First number.
            b (int): Second number.

        Returns:
            int: The greatest common divisor of a and b.
        """
        while a != 0:
            a, b = b % a, a
        return b

    def _find_mod_inverse(self, a: int, m: int) -> Optional[int]:
        """
        Finds the modular inverse of a modulo m using the extended Euclidean algorithm.

        Args:
            a (int): The number for which the modular inverse is needed.
            m (int): The modulus.

        Returns:
            Optional[int]: The modular inverse of 'a' mod 'm' if it exists, else None.
        """
        if self._gcd(a, m) != 1:
            return None  # No modular inverse exists
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
