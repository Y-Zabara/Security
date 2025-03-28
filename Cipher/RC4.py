import codecs
import itertools

MOD = 256  # Size of the S-block (permutation array)


class RC4Keystream:
    """
    Implements the keystream generator for the RC4 stream cipher.
    """
    def __init__(self, key):
        """
        Initializes the RC4 keystream generator.

        Args:
            key (str): The encryption key.
        """
        self.key = [ord(c) for c in key]  # Convert key characters to ASCII values
        self.S = self.KSA()  # Initialize the permutation array
        self.i = 0  # Index i for PRGA
        self.j = 0  # Index j for PRGA

    def KSA(self):
        """
        Key-Scheduling Algorithm (KSA): Initializes the permutation array.

        Returns:
            list: The initialized S-block (permutation array).
        """
        S = list(range(MOD))  # Initialize S with values 0 to 255
        j = 0
        for i in range(MOD):
            j = (j + S[i] + self.key[i % len(self.key)]) % MOD
            S[i], S[j] = S[j], S[i]  # Swap values in S
        return S

    def __iter__(self):
        """
        Makes the keystream generator an iterable object.

        Returns:
            self: The instance itself as an iterator.
        """
        return self

    def __next__(self):
        """
        Pseudo-Random Generation Algorithm (PRGA):
        Generates the next byte of the keystream.

        Returns:
            int: The next byte from the keystream.
        """
        self.i = (self.i + 1) % MOD
        self.j = (self.j + self.S[self.i]) % MOD
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]  # Swap values
        return self.S[(self.S[self.i] + self.S[self.j]) % MOD]


class RC4:
    """
    Implements the RC4 encryption and decryption algorithm.
    """
    def __init__(self, key: str) -> None:
        """
        Initializes the RC4 cipher with a given key.

        Args:
            key (str): The encryption key.
        """
        self.key: str = key
        self.keystream = None
        self.alphabet = "abcdefghklmnopqrt"  # Allowed characters for brute-force attack

    def _encrypt_logic(self, text):
        """
        Core encryption/decryption logic using XOR with keystream bytes.

        Args:
            text (list[int]): List of ASCII values of characters in plaintext or ciphertext.

        Returns:
            str: The encrypted or decrypted hexadecimal string.
        """
        self.keystream = iter(RC4Keystream(self.key))
        res = []
        for c in text:
            val = "%02X" % (c ^ next(self.keystream))  # XOR operation with keystream byte
            res.append(val)
        return "".join(res)

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts the given plaintext using RC4.

        Args:
            plaintext (str): The message to be encrypted.

        Returns:
            str: The encrypted ciphertext in hexadecimal format.
        """
        plaintext = [ord(c) for c in plaintext]  # Convert characters to ASCII values
        return self._encrypt_logic(plaintext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts the given ciphertext using RC4.

        Args:
            ciphertext (str): The encrypted message in hexadecimal format.

        Returns:
            str: The decrypted plaintext message.
        """
        ciphertext = codecs.decode(ciphertext, "hex_codec")  # Convert hex to bytes
        res = self._encrypt_logic(ciphertext)  # Apply RC4 encryption (same operation as encryption)
        return codecs.decode(res, "hex_codec").decode("utf-8")  # Decode back to string

    def brute_force_decrypt(self, ciphertext: str):
        """
        Attempts to brute-force decrypt the given ciphertext by trying all possible keys.

        Args:
            ciphertext (str): The encrypted message in hexadecimal format.
        """
        for key_tuple in itertools.product(self.alphabet, repeat=len(self.key)):
            key = "".join(key_tuple)
            self.keystream = iter(RC4Keystream(key))
            try:
                decrypted_text = self.decrypt(ciphertext)
            except Exception:
                continue



if __name__ == "__main__":
    key = "nota"
    plaintext = "Hello, RC4!hfdlllllsslsllsllslslsllslsllslsllssls"

    rc4 = RC4(key)

    ciphertext = rc4.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")

    decrypted = rc4.decrypt(ciphertext)
    print(f"Decrypted: {decrypted}")
    rc4.brut_force_decrypt(ciphertext)

    assert plaintext == decrypted, "Error: Decryption failed!"
