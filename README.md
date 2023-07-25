Disclaimer:

This ransomware is not to be used in a manner harmful to any systems whatsoever.

Its purpose is for demonstration and to share awareness about programming, malware, and cryptography.

Be aware that you could encrypt your files and be unable to decrypt them - use at your own risk!

--

What is Ransomware?

Ransomware prevents the legitimate users of a system from accessing their device or data, usually by strong encryption, and demands payment in exchange for the decryption key.

It is becoming more widespread as time goes on.

To be successful ransomware must not have a hardcoded decryption key which can be accessed by decompiling the binary code.

This way, only a single individual has access to the single-use decryption key.

--

This code demonstrates the mixed use of asymmetric public-key cryptography to hide and send the decryption key back to the C2 (command-and-control server) in an encrypted format.

It automatically generates a symmetric encryption key on the target host, encrypts it with the public key (which was generated before on the C2), and sends that to C2.

The C2 then uses the matching private key to decrypt the symmetric key, and makes a request to the blockchain.info API to see if a payment has been made to the bitcoin address.

If a payment of a specified amount has been made, it then automatically sends the decrypted symmetric key back to the target host and uses it to automatically decrypt the files.

--

Usage:

To run locally, using a single computer as C2 and target, set SERVER_IP in server.py and client.py to localhost.

If you wish to run over LAN or WAN you'll have to change settings in your firewall and/or make port forwards in your router accordingly.

Start server.py on your C2 machine which will open a socket to listen on.

Run encrypt.py on your target which will generate a symmetric encryption key, use it to encrypt file_to_encrypt.txt, and finally encrypt the symmetric key itself using public_key.pem. It will then be saved on the target machine (only in encrypted form) as encrypted_symmetric_key.key.

Finally, run client.py on target machine. client.py will get the contents of encrypted_symmetric_key.key, connect to the C2 machine over the socket it will be listening on, and send it the encrypted symmetric key.

server.py will receive encrypted_symmetric_key.key, decrypt it using the private key only it has, and save this as decrypted_symmetric_key.key.

It will check the given bitcoin address on blockchain.info for payment (I selected a random, highly active bitcoin address and amount > 0 for this so it should automatically release the payment).

If payment has been made, it will then send decrypted_symmetric_key.key to client.py which is still running on the target machine.

Finally, client.py will use decrypted_symmetric_key.key to decrypt file_to_encrypt.txt.
