# BOB ( reciever )

from socket import *
import struct
from RSA_Socket import decrypt, d, p, q 

serverPort = 12000
serverIP = '127.0.0.1'
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort)) # server name is ip and port
print("listining at  : ", serverSocket.getsockname())

serverSocket.listen(1)
while True:
    #serverSocket.listen(1)
    connectionSocket, addr = serverSocket.accept()
    print("server ", connectionSocket.getsockname())
    print(" socket connection between ", serverSocket.getsockname(), " and ", connectionSocket.getsockname())

    byte_recieved_data = connectionSocket.recv(4096)

    # Unpack the received data in bytes into a list of integers directly
    # user_ciphertext_int_list = list(struct.unpack('!{}i'.format(len(byte_recieved_data) // struct.calcsize('i')), byte_recieved_data))

    # decode string then convert it to list
    byte_recieved_data = byte_recieved_data.decode()
    user_ciphertext_int_list = [ord(char) for char in byte_recieved_data]

    print(' Recieved message from client is : ', user_ciphertext_int_list)
  
    decrypted_text = decrypt(user_ciphertext_int_list, d, p, q)
    print(' decryption is : ', decrypted_text)

    connectionSocket.send(decrypted_text.encode()) #('utf-8', errors='replace')
    connectionSocket.close()












# sentence = connectionSocket.recv(1024)
#     #    capitalizedSentence= sentence.decode()
#     print(' Recieved message from client is : ', sentence.decode())
#     realmessage = sentence.decode()
#     size = str(len(realmessage))
#     connectionSocket.send(size.encode())
#     #    size = len((sentence.encode('utf-8')))
#     #    connectionSocket.send(str(size.encode()))
#     #    print('size of client message is : ' , size)
#     #    connectionSocket.send(capitalizedSentence.encode())
