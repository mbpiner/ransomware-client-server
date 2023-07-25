import socket
import cryptocode


# This should also be set to the local, private IP address of your server to run in your LAN.
# Set this to localhost in client.py and server.py to run locally on one machine.
# Running like this in LAN won't require a port forward, just a temporary firewall opening.

SERVER_IP = "192.168.1.150" 


def decrypt_file(file_path, key):
    with open(file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    # Decrypt the encrypted data using the key
    # Notice that we're now decoding the encrypted data before using it - 
    # We decoded the key in the last step so we don't have to do it here.
    decrypted_data = cryptocode.decrypt(encrypted_data.decode('latin-1'), key)
    
    # Notice that we're now encoding the decrypted data back to bytes before writing to the file
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data.encode('latin-1'))


def main():
    HOST, PORT = SERVER_IP, 8001

    with open("encrypted_symmetric_key.key", "rb") as key_file:
        encrypted_key = key_file.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(encrypted_key)

        response = client_socket.recv(1024)
        response_decoded = response.decode('latin-1')
        decrypt_file("file_to_encrypt.txt", response_decoded)
        print('Files have been successfully decrypted. \n')

if __name__ == "__main__":
    main()
