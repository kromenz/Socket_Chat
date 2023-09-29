import socket
import errno
import sys
import threading
import os
import time

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
os.system('cls')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

server_response = None

def menu():
    print("\nMenu:")
    print("1. Enter Chat Room")
    print("2. Calculator")
    print("3. Exit")
    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        os.system('cls')
        print("'/back', to return to the previous menu")
        while True:
            message = input(f'{my_username} > ')
            if message == '/back':
                os.system('cls')
                break
            else:
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)

    elif choice == '2':
        os.system('cls')
        calculator()

    elif choice == '3':
        os.system('cls')
        client_socket.send('/exit'.encode('utf-8'))
        print("\n\tThank you for visiting!")
        time.sleep(5)
        sys.exit()

    else:
        print("Invalid choice. Please choose 1, 2, or 3.")

def calculator():
    os.system('cls')
    while True:
        print("\nCalculator Menu:")
        print("1. Calculate")
        print("2. Exit Calculator")

        calc_choice = input("Choose an option (1/2): ")

        if calc_choice == '1':
            os.system('cls')
            print("\nCalculator:")

            expression = input("Enter a mathematical expression: ")
            try:
                result = eval(expression)
                result_str = str(result)
                message_type = "calc_result"
                message = f"{message_type}{result_str}".encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
                print(f"\nThe result of the calculation is {result_str}")
                time.sleep(3)
            except Exception as e:
                print(f"Error calculating expression: {e}")

        elif calc_choice == '2':
            client_socket.send('/exit'.encode('utf-8'))
            os.system('cls')
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")

def receive_messages():
    while True:
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Display the message on a new line
            print(f'\n{username} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error: {}'.format(str(e)))
                sys.exit()
            continue

        except Exception as e:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

# Start the message receiving thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

while True:
    try:
        # Try to receive the server response
        server_response = client_socket.recv(HEADER_LENGTH).decode('utf-8').strip()
    except BlockingIOError:
        pass

    # Check if server_response is set (not None)
    if server_response:
        if server_response == 'full':
            print("Server is full. Please wait for a vacancy.")
            
            # Continue waiting until a vacancy is available
            while True:
                try:
                    server_response = client_socket.recv(HEADER_LENGTH).decode('utf-8').strip()
                    if server_response != 'full':
                        break
                except BlockingIOError:
                    pass
        break  # Exit the loop when a valid response is received
    else:
        menu()
