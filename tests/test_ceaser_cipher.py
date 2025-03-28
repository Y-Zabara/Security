import pytest
from Cipher.Caesar import CaesarCipher  

@pytest.mark.parametrize("alphabet, key, plain, encrypted", [
    # Латиниця (англійський алфавіт)
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "Hello", "Khoor"),
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "Python", "SBwkrq"),
    # Латиниця з циклічним зсувом (Z -> C)
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "XYZ", "abc"),

    # Кирилиця (українська абетка)
    ("АБВГДЕЄЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ", 5, "ПРИВІТ", "ФХНЖІЧ"),
    ("АБВГДЕЄЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ", 5, "ЩОДЕННИК", "БУИЙТТНП"),

    # Цифри
    ("0123456789", 4, "1234", "5678"),
    ("0123456789", 7, "9876", "6543"),

    # Спеціальні символи
    ("!@#$%^&*()", 2, "!@#", "#$%"),
    ("!@#$%^&*()", 5, "&*()", "@#$%"),
])
def test_encrypt(alphabet, key, plain, encrypted):
    cipher = CaesarCipher(alphabet, key)
    assert cipher.encrypt(plain) == encrypted

@pytest.mark.parametrize("alphabet, key, encrypted, plain", [
    # Латиниця
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "Khoor", "Hello"),
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "SBwkrq", "Python"),
    ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 3, "abc", "XYZ"),

    # Кирилиця
    ("АБВГДЕЄЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ", 5, "ФХНЖЧ", "ПРИВТ"),
    ("АБВГДЕЄЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯ", 5, "БУИЙТТНП", "ЩОДЕННИК"),

    # Цифри
    ("0123456789", 4, "5678", "1234"),
    ("0123456789", 7, "6543", "9876"),

    # Спеціальні символи
    ("!@#$%^&*()", 2, "#$%", "!@#"),
])
def test_decrypt(alphabet, key, encrypted, plain):
    cipher = CaesarCipher(alphabet, key)
    assert cipher.decrypt(encrypted) == plain

