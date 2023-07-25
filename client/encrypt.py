import os
import socket
import secrets
import cryptography.hazmat.primitives.asymmetric as asymmetric
import cryptography.hazmat.primitives.ciphers as ciphers
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend 
import cryptocode

def generate_symmetric_key():
    symmetric_key = secrets.token_bytes(32)
    return symmetric_key

def load_public_key(path="public_key.pem"):
    with open(path, "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(public_key_file.read(), backend=default_backend())
    return public_key

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

         # Notice that we're now decoding the plaintext and the key before using them because that is what cryptocode's encrypt() function calls for.
    
    encrypted_data = cryptocode.encrypt(plaintext.decode('latin-1'), key.decode('latin-1'))
    
    with open(file_path, 'wb') as encrypted_file:


        # Notice that we're now encoding the data cryptocode's encrypt() function returned to us back to bytes before writing to the file.

        encrypted_file.write(encrypted_data.encode('latin-1'))

def encrypt_symmetric_key(symmetric_key):
    public_key = load_public_key()

    encrypted_key = public_key.encrypt(
        symmetric_key,
        asymmetric.padding.OAEP(
            mgf=asymmetric.padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open("encrypted_symmetric_key.key", "wb") as encrypted_key_file:
        encrypted_key_file.write(encrypted_key)

def main():
    symmetric_key = generate_symmetric_key()

    file_to_encrypt_path = 'file_to_encrypt.txt'

    encrypt_file(file_to_encrypt_path, symmetric_key)

    encrypt_symmetric_key(symmetric_key)

if __name__ == "__main__":
    main()

    
    












