import socket
import threading
import sys
import time

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 1234))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break
        
def write():
    while True:
        message = input('')
        if message == "/back":
            print("You have left the chat.")
            client.send("0".encode('ascii'))  # Envie 0 para o servidor como sinal de desconexão
            client.close()
            break
        else:
            message = '{}: {}'.format(nickname, message)
            client.send(message.encode('ascii'))
      
# # Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start() 

write_thread = threading.Thread(target=write)
write_thread.start()