import os
import socket
import time

# Configurações do cliente
host = '127.0.0.1'  # Endereço IP do servidor
port = 12345       # Porta do servidor

# Criação do socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta-se ao servidor
    client_socket.connect((host, port))
except socket.error as msg:
    print('Erro ao conectar ao servidor: ' + str(msg))
    exit()
    
# Função para obter a escolha do usuário
def obter_escolha():
    print("\n\tEscolha uma opção:")
    print("\t1. Introduzir uma expressão")
    print("\t2. Sair do programa")
    escolha = input("\tOpção (1 / 2): ")
    os.system('cls')
    return escolha

while True:
    escolha = obter_escolha()

    # Envia a escolha para o servidor
    client_socket.send(escolha.encode('utf-8'))

    if escolha == '1':
        
        # Solicita ao usuário uma expressão matemática
        expressao = input('Digite uma expressão matemática: ')
        
        try:
            # Envia a expressão para o servidor
            client_socket.send(expressao.encode('utf-8'))
        except:
            print("Ocorreu um erro ao enviar a expressão...")
            continue

        # Recebe o resultado do servidor
        resultado = client_socket.recv(1024).decode('utf-8')
        print('Resultado: ' + resultado)
        time.sleep(5)
        os.system('cls')
    elif escolha == '2':
        # Opção para sair do programa
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Escolha 1 para introduzir uma expressão ou 2 para sair do programa.")

# Fecha a conexão com o servidor
client_socket.close()
