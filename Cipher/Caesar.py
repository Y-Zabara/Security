import time


def timing_decorator(func):
    """
    A decorator that measures and returns the execution time of a function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function that returns a tuple (execution_time, result).
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start measuring time
        result = func(*args, **kwargs)
        end_time = time.perf_counter()  # End measuring time
        execution_time = end_time - start_time
        return execution_time, result
    return wrapper


class CaesarCipher:
    """
    A class implementing the Caesar cipher for encryption and decryption.

    Attributes:
        alphabet (str): The alphabet used for shifting characters.
        key (int): The shift value for encryption and decryption.
    """

    def __init__(self, alphabet: str, key: int) -> None:
        """
        Initializes the CaesarCipher with a given alphabet and key.

        Args:
            alphabet (str): The alphabet to be used for shifting.
            key (int): The shift value.
        """
        self.alphabet: str = alphabet
        self.key: int = key

    def encrypt(self, message: str) -> str:
        """
        Encrypts a message using the Caesar cipher.

        Args:
            message (str): The plaintext message to encrypt.

        Returns:
            str: The encrypted message.
        """
        result = ""
        for symbol in message:
            if symbol in self.alphabet:
                symbol_index = self.alphabet.find(symbol)
                translated_index = (symbol_index + self.key) % len(self.alphabet)
                result += self.alphabet[translated_index]
            else:
                result += symbol  # Preserve characters that are not in the alphabet
        return result

    def decrypt(self, message: str) -> str:
        """
        Decrypts a message encrypted with the Caesar cipher.

        Args:
            message (str): The encrypted message.

        Returns:
            str: The decrypted message.
        """
        result = ""
        for symbol in message:
            if symbol in self.alphabet:
                symbol_index = self.alphabet.find(symbol)
                translated_index = (symbol_index - self.key) % len(self.alphabet)
                result += self.alphabet[translated_index]
            else:
                result += symbol  # Preserve characters that are not in the alphabet
        return result

    @timing_decorator
    def brute_force_decrypt(self, message: str) -> str:
        """
        Attempts to brute-force decrypt a message by trying all possible keys.

        Args:
            message (str): The encrypted message.

        Returns:
            str: The possible decryption results with different keys.
        """
        result = ""
        original_key = self.key
        for key in range(len(self.alphabet)):
            self.key = key
            translated = self.decrypt(message)
            result += f"Key {key}: {translated}\n"
        self.key = original_key
        return result


if __name__ == "__main__":
    # Define the alphabet and create an instance of CaesarCipher
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    cipher = CaesarCipher(alphabet, 3)

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
    execution_time, hacker_result = cipher.hacker_crypt(encrypted)
    print(f"Hacker attempt (brute force):\n{hacker_result}")
    print(f"Execution time: {execution_time:.6f} seconds")

