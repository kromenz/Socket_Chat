import os
import socket
import threading
import time

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)
        
# Handling Messages From Clients
def handle(client):
    address = client.getpeername()  # Obtém o endereço IP e a porta do cliente
    while True:
        try:
            # Broadcasting Messages
            msg = message = client.recv(1024)
            client_address = f"{address[0]}:{address[1]}"  # Obtém o endereço IP e a porta do cliente
            
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':     
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
                    
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned!')
                else:
                    client.send('Command was refused!'.encode('ascii'))
            
            elif msg.decode('ascii').startswith('LIST'):
                if nicknames[clients.index(client)] == 'admin':
                    client.send("\nConnected Clients:\n".encode('ascii') + ", ".join(nicknames).encode('ascii'))
                else:
                    client.send('Command was refused!'.encode('ascii'))
                    
            else:
                print(f"{client_address} > {message}")
                broadcast(message)
            
        except:
            # Removing And Closing Clients
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                print(f"{nickname} disconnected from the server!")
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
                break
        
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        # print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        if nickname == "admin":
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != "123":
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue 
            
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(f"Nickname is {nickname} connected from {str(address)}")
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked by an admin'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an admin'.encode('ascii'))
    else:
        admin_client = clients[nicknames.index('admin')]
        admin_client.send(f'User {name} not found'.encode('ascii'))
        
print(f"Server listening on {host} : {port}...")
receive()