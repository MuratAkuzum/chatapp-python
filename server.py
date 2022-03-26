import socket, threading

HOST = "127.0.0.1"
PORT = 12345
SIZE = 1024
FORMAT = 'utf-8'

client_list = {}

def broadcast(message):
    for client in client_list.values():
        client.send(message.encode(FORMAT))

def client_login(client_socket):
        client_socket.send("Welcome to the server. Please enter a username:".encode(FORMAT))

        while True:
            username = client_socket.recv(SIZE).decode(FORMAT)
            if username not in client_list:
                client_list[username] = client_socket
                print(f"Username: {username} \nAddress: {client_socket.getpeername()[0]}")
                print(f"{client_list}")
                break
            else:
                client_socket.send("Username is already taken, please enter another name:".encode(FORMAT))
        return username

def client_logoff(username, client_socket):
        try:
            client_list.pop(username, client_socket)
            client_socket.close()
        except:
            print("Error while trying to log off the client!")

def handle_client(client_socket, client_addr):
        print(f"{client_list}")
        username = client_login(client_socket)
        print(f"{username} connected with {client_socket.getpeername()[0]}!")

        while True:
            data_received = client_socket.recv(SIZE).decode(FORMAT)
            print(f"{username} sends: {data_received}")

            if len(data_received) == 0:
                client_socket.send("Exit request received, closing connection...".encode(FORMAT))
                client_logoff(username, client_socket)
                print(f"{client_list}")
                break
            elif data_received == "/quit":
                broadcast(f"{username} has just left the server!")
                client_socket.send("Exit request received, closing connection...".encode(FORMAT))
                client_logoff(username, client_socket)
                print(f"{client_list}")
                break
            elif data_received == "/who":
                client_socket.send(f"{client_list.keys()}".encode(FORMAT))
            else:
                continue

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:    
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started listening on {HOST}:{PORT} for client connection...")
    except:
        print("Server failed to start, try again!")
        server.shutdown(socket.SHUT_RDWR)
        server.close()

    while True:
        client_socket, client_addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr), daemon=True)
        thread.start()
        print(f"Current active connections: {threading.active_count() -1}")

    server.shutdown(socket.SHUT_RDWR)
    server.close()

def main():
    run_server()

if __name__ == '__main__':
    main()


# TODO: Clean up the names show up in /who broadcast message
# TODO: Add more commands