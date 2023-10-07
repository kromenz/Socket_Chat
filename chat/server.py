import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 1234

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message, client):
    for c in clients:
        if c != client:
            c.send(message)

def handle(client):
    address = client.getpeername()  # Obtém o endereço IP e a porta do cliente
    while True:
        try:
            # Receber mensagem do cliente
            message = client.recv(1024).decode('ascii')
            # print(message)
            client_address = f"{address[0]}:{address[1]}"  # Obtém o endereço IP e a porta do cliente
            msg = str(message)
            if msg == "0":  # Verifica se o cliente enviou 0 como sinal de desconexão
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} has left the chat!'.format(nickname).encode('ascii'), client)
                nicknames.remove(nickname)
                break  # Sair do loop quando o cliente sair

            # Enviar a mensagem para todos os outros clientes
            print(f"{client_address} > {message}")
            broadcast(message, client)
            
        except:
            # Remover e fechar clientes em caso de erro
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'), client)
            nicknames.remove(nickname)
            # Não é necessário chamar break aqui, pois o loop continuará a ouvir outras mensagens
            continue  # Continue ouvindo outras mensagens

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("{} has joined the server".format(nickname))
        broadcast("{} joined the chat!".format(nickname).encode('ascii'), client)
        client.send('Connected to server ("/back" to exit)!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
print(f"Server listening on {host}:{port}...")
receive()