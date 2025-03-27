import codecs
import itertools


MOD = 256  # Розмір S-блоку


class RC4Keystream:
    def __init__(self, key):
        self.key = [ord(c) for c in key]
        self.S = self.KSA()
        self.i = 0
        self.j = 0

    def KSA(self):
        """Алгоритм ключового планування (Key Scheduling Algorithm)."""
        S = list(range(MOD))
        j = 0
        for i in range(MOD):
            j = (j + S[i] + self.key[i % len(self.key)]) % MOD
            S[i], S[j] = S[j], S[i]
        return S

    def __iter__(self):
        """Додає підтримку ітератора."""
        return self

    def __next__(self):
        """Генерує наступний байт ключового потоку (PRGA)."""
        self.i = (self.i + 1) % MOD
        self.j = (self.j + self.S[self.i]) % MOD
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]
        return self.S[(self.S[self.i] + self.S[self.j]) % MOD]


class RC4:
    def __init__(self, key: str) -> None:
        self.key: str = key
        self.keystream = None
        self.alphabet = "abcdefghklmnopqrt"

    def _encrypt_logic(self, text):
        self.keystream = iter(RC4Keystream(self.key))
        res = []
        for c in text:
            val = "%02X" % (c ^ next(self.keystream))  # XOR операція
            res.append(val)
        return "".join(res)

    def encrypt(self, plaintext):
        plaintext = [ord(c) for c in plaintext]
        return self._encrypt_logic(plaintext)

    def decrypt(self, ciphertext):
        ciphertext = codecs.decode(ciphertext, "hex_codec")
        res = self._encrypt_logic(ciphertext)
        return codecs.decode(res, "hex_codec").decode("utf-8")

    def brut_force_decrypt(self, ciphertext):
        for key_tuple in itertools.product(self.alphabet, repeat=len(self.key)):
            key = "".join(key_tuple)
            self.keystream = iter(RC4Keystream(key))
            try:
                decrypted_text = self.decrypt(ciphertext)
            except Exception:
                continue  # Пропускаємо помилки


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
