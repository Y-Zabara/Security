#!/bin/env python
import argparse
import os
from rsa import newkeys, encrypt, decrypt, PublicKey, PrivateKey
from repositories import RegularFileRepo

# Генерація RSA ключів і їх збереження в файлі
def genkeys():
    public_key, private_key = newkeys(512)  # Створення пари ключів (512 біт)

    public_key_file = RegularFileRepo(filename="keyfile.pub")
    private_key_file = RegularFileRepo(filename="keyfile.prvt")

    public_key_file.save_bytes(public_key.save_pkcs1())  # Збереження публічного ключа
    private_key_file.save_bytes(private_key.save_pkcs1())  # Збереження приватного ключа
    print(f"Keys have been saved to {private_key_file.filename, public_key_file.filename}")

# Зчитування ключів з файлу
def load_keys(keyfile, reader):
    with open(keyfile, "rb") as keyf:
        key = reader(keyf.read())
    return key

# Шифрування тексту з використанням публічного ключа
def encrypt_text(keyfile, message=None, file=None):
    public_key = load_keys(keyfile, PublicKey.load_pkcs1)

    if message:
        ciphertext = encrypt(message.encode(), public_key)
        print(ciphertext.hex())
    elif file:
        with open(file, "r") as f:
            message = f.read()
            ciphertext = encrypt(message.encode(), public_key)

# Дешифрування тексту з використанням приватного ключа
def decrypt_text(keyfile, message=None, file=None):
    private_key = load_keys(keyfile, PrivateKey.load_pkcs1)

    if file:
        try:
            with open(file, "r") as f:
                message = f.read().strip()
        except FileNotFoundError:
            print(f"Error: The file {file} does not exist.")
            return
    elif message:
        ciphertext = bytes.fromhex(message)
        try:
            plaintext = decrypt(ciphertext, private_key).decode()
            print(plaintext)
        except Exception as e:
            print(f"Error during decryption: {str(e)}")
    else: print("Message don`t be void")


# Основна функція для обробки команд
def main():
    parser = argparse.ArgumentParser(description="Simple RSA Encryption CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Команда для генерації ключів
    genkeys_parser = subparsers.add_parser("genkeys", help="Generate RSA keys and save them to a file")

    # Команда для шифрування
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a message or text file")
    encrypt_parser.add_argument("-k", "--keyfile", required=True, help="RSA key file")
    group = encrypt_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="File with the message to encrypt")
    group.add_argument("-m", "--message", help="Message to encrypt")

    # Команда для дешифрування
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a ciphertext")
    decrypt_parser.add_argument("-k", "--keyfile", required=True, help="RSA key file")
    group = decrypt_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="File with the message to decrypt")
    group.add_argument("-m", "--message", help="Message to decrypt")


    args = parser.parse_args()

    if args.command == "genkeys":
        genkeys()
    elif args.command == "encrypt":
        encrypt_text(args.keyfile, message=args.message, file=args.file)
    elif args.command == "decrypt":
        decrypt_text(args.keyfile, message=args.message, file=args.file)

if __name__ == "__main__":
    main()
