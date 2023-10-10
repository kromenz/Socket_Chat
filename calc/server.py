import socket
import sys

# Configurações do servidor
host = '127.0.0.1'  # Endereço IP do servidor
port = 12345       # Porta do servidor

# Criação do socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Vincula o socket à porta e ao endereço IP
    server_socket.bind((host, port))
except socket.error as msg:
    print('Erro ao vincular o socket: ' + str(msg))
    sys.exit()

# Coloca o servidor no modo de escuta
server_socket.listen(5)

print('Aguardando conexões...')


# Função para avaliar a expressão matemática
def calcular(expressao):
    try:
        resultado = eval(expressao)
        return str(resultado)
    except:
        return "Erro na expressão"

while True:
    # Aceita uma conexão de cliente
    client_socket, addr = server_socket.accept()
    print('Conexão estabelecida com ' + addr[0] + ':' + str(addr[1]))

    while True:
        # Receber a escolha do cliente
        escolha = client_socket.recv(1024).decode('utf-8')

        if escolha == '1':
            # Recebe a expressão do cliente
            expressao = client_socket.recv(1024).decode('utf-8')
            # Calcula o resultado da expressão
            resultado = calcular(expressao)
            
            print(f'Expressão recebida por {addr}: ' + expressao + ' = ' + resultado)

            # Envia o resultado de volta para o cliente
            client_socket.send(resultado.encode('utf-8'))
        elif escolha == '2':
            # Opção para sair do programa
            print(f'Cliente {addr} saiu do programa.')
            break
        else:
            print(f'Cliente {addr} escolheu uma opção inválida.')

    # Fecha a conexão com o cliente
    client_socket.close()
