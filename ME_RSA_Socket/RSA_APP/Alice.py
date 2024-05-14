# Alice ( sender )

from socket import *
import struct
from RSA_Socket import encrypt, e, n

serverIP= '127.0.0.1'
serverPort= 12000
while True:
    sentence = input(" enter sentence to dycrept or (exit) to disconnect : ")
    if sentence=="exit" :
        exit()
    else:
        clientSocket= socket(AF_INET, SOCK_STREAM)
        #clientSocket.bind(('127.0.0.1',0)) # binding port 0 mean use any port this is should not be stable
        clientSocket.connect((serverIP, serverPort))
       
        encrypted_sentence = encrypt(sentence,e,n)
        print("data that will be sent:\t", encrypted_sentence)

        # # Convert the list of integers to bytes directly
        #encrypted_as_byte_data = struct.pack('!{}i'.format(len(encrypted_sentence)), *encrypted_sentence)
        
        # convert to string then byte and reverse there
        encrypted_sentence = ''.join(map(chr, encrypted_sentence))
        encrypted_as_byte_data = encrypted_sentence.encode() #('utf-8', errors='replace')

        clientSocket.sendall(encrypted_as_byte_data)

        decrypted_message = clientSocket.recv(4096)
        print ('  recieved dycrepted message FromServer : ' , decrypted_message.decode())#decode('utf-8'))
        clientSocket.close()
