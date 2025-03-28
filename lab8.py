#!/bin/env python
import argparse
import os
from ecdsa import SigningKey, VerifyingKey, NIST256p
from ecdsa.util import sigencode_der, sigdecode_der
from repositories import RegularFileRepo
from hashlib import sha256

# Генерація ключів ECDSA і їх збереження в файлі
def genkeys():
    sk = SigningKey.generate(curve=NIST256p)  # Генерація приватного ключа
    vk = sk.get_verifying_key()  # Отримання публічного ключа

    public_key_file = RegularFileRepo(filename="keyfile.pub")
    private_key_file = RegularFileRepo(filename="keyfile.prvt")

    public_key_file.save_bytes(vk.to_pem())  # Збереження публічного ключа
    private_key_file.save_bytes(sk.to_pem())  # Збереження приватного ключа
    print(f"Keys have been saved to {private_key_file.filename, public_key_file.filename}")

# Зчитування ключів з файлу
def load_keys(keyfile, reader):
    with open(keyfile, "rb") as keyf:
        key = reader(keyf.read())
    return key

# Підписування тексту з використанням приватного ключа ECDSA
def sign_text(keyfile, message=None, file=None, signature_file=None):
    private_key = load_keys(keyfile, SigningKey.from_pem)

    if message:
        signature = private_key.sign(message.encode(), hashfunc=sha256, sigencode=sigencode_der)
        print("Signature generated:", signature.hex())
    elif file:
        with open(file, "r") as f:
            message = f.read().strip()
            signature = private_key.sign(message.encode(), hashfunc=sha256, sigencode=sigencode_der)
            print("Signature generated:", signature.hex())
    
    # Якщо вказано файл для збереження підпису
    if signature_file:
        with open(signature_file, "wb") as sigf:
            sigf.write(signature)
        print(f"Signature has been saved to {signature_file}")

# Перевірка підпису з використанням публічного ключа ECDSA
def verify_signature(keyfile, message=None, signature=None, file=None):
    public_key = load_keys(keyfile, VerifyingKey.from_pem)

    if file:
        try:
            with open(file, "r") as f:
                message = f.read().strip()
        except FileNotFoundError:
            print(f"Error: The file {file} does not exist.")
            return
    if signature:
        try:
            with open(signature, "rb") as f:  # Читання підпису як байтів
                signature = f.read()
            if not signature:
                print("Error: Signature file is empty.")
                return
        except FileNotFoundError:
            print(f"Error: The file {file} does not exist.")
            return
        #signature = bytes.fromhex(signature)
    else:
        print("Message and signature cannot be empty")
        return

    try:
        public_key.verify(signature, message.encode(), hashfunc=sha256, sigdecode=sigdecode_der)
        print("Signature is valid")
    except Exception as e:
        print(f"Signature verification failed: {str(e)}")

# Основна функція для обробки команд
def main():
    parser = argparse.ArgumentParser(description="Simple ECDSA Signature CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Команда для генерації ключів
    genkeys_parser = subparsers.add_parser("genkeys", help="Generate ECDSA keys and save them to a file")

    # Команда для підписування
    sign_parser = subparsers.add_parser("sign", help="Sign a message or text file")
    sign_parser.add_argument("-k", "--keyfile", required=True, help="ECDSA key file")
    sign_parser.add_argument("-s", "--signature-file", help="File to save the generated signature")
    group = sign_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="File with the message to sign")
    group.add_argument("-m", "--message", help="Message to sign")

    # Команда для перевірки підпису
    verify_parser = subparsers.add_parser("verify", help="Verify a signature")
    verify_parser.add_argument("-k", "--keyfile", required=True, help="ECDSA key file")
    verify_parser.add_argument("-s", "--signature", required=True, help="Signature to verify")
    group = verify_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="File with the message to verify")
    group.add_argument("-m", "--message", help="Message to verify")

    args = parser.parse_args()

    if args.command == "genkeys":
        genkeys()
    elif args.command == "sign":
        sign_text(args.keyfile, message=args.message, file=args.file, signature_file=args.signature_file)
    elif args.command == "verify":
        verify_signature(args.keyfile, message=args.message, signature=args.signature, file=args.file)

if __name__ == "__main__":
    main()
