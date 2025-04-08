from Cipher.Caesar import CaesarCipher


class DoubleCaesarCipher:
    def __init__(self, alphabet: str, key: tuple) -> None:
        self.keys: tuple = key
        self.caesar_cipher = CaesarCipher(alphabet, key[0])

    def encrypt(self, message: str):
        self.caesar_cipher.key = self.keys[0]
        encrypted_message = self.caesar_cipher.encrypt(message)
        self.caesar_cipher.key = self.keys[1]
        return self.caesar_cipher.encrypt(encrypted_message)

    def decrypt(self, message: str):
        self.caesar_cipher.key = self.keys[0]
        encrypted_message = self.caesar_cipher.decrypt(message)
        self.caesar_cipher.key = self.keys[1]
        return self.caesar_cipher.decrypt(encrypted_message)

    def brute_force_decrypt(self, message: str):
        return self.caesar_cipher.brute_force_decrypt(message)

if __name__ == "__main__":
    # Define the alphabet and create an instance of CaesarCipher
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    cipher = DoubleCaesarCipher(alphabet, (3, 5))

    # Original message
    text = "Hello, World!"

    # Encrypt and decrypt the message
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)

    # Print results
    print(f"Original: {text}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

    # Attempt to brute-force decrypt the message and measure execution time
    execution_time, hacker_result = cipher.brute_force_decrypt(encrypted)
    print(f"Hacker attempt (brute force):\n{hacker_result}")
    print(f"Execution time: {execution_time:.6f} seconds")

