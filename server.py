import socket, threading

HOST = "127.0.0.1"
PORT = 12345
SIZE = 1024
FORMAT = 'utf-8'

client_list = {}

class Client:
    def __init__(self, username, client_addr, client_socket, online, connected):
        self.username = username
        self.client_addr = client_addr
        self.client_socket = client_socket
        self.online = bool
        self.connected = bool

    def client_login():
        Client.client_socket.send("Welcome to the server. Please enter a username:".encode(FORMAT))

        while True:
            username = Client.client_socket.recv(SIZE).decode(FORMAT)
            if username not in client_list:
                Client.username = username
                Client.online = True
                client_list[Client.username] = Client.client_socket
                print(f"Username: {Client.username} \nAddress: {Client.client_socket.getpeername()[0]}")
                print(f"{client_list}")
                Client.connected = True
                break
            else:
                Client.client_socket.send("Username is already taken, please enter another name:".encode(FORMAT))
    
    def client_logoff():
        try:
            Client.online = False
            Client.connected = False
            client_list.pop(Client.username, Client.client_socket)
            Client.client_socket.close()
        except:
            print("Error while trying to log off the client!")

    def handle_client(client_socket, client_addr):
        print(f"{client_list}")
        Client.client_login()

        print(f"{Client.username} connected with {Client.client_socket.getpeername()[0]}!")


        while Client.connected:
            data_received = Client.client_socket.recv(SIZE).decode(FORMAT)
            print(f"{Client.username} sends: {data_received}")

            if len(data_received) == 0:
                Client.client_socket.send("Exit request received, closing connection...".encode(FORMAT))
                Client.client_logoff()
                print(f"{client_list}")
                break

            elif data_received == "/quit":
                broadcast("Someone has just left the server!")
                Client.client_socket.send("Exit request received, closing connection...".encode(FORMAT))
                Client.client_logoff()
                print(f"{client_list}")
                break

            else:
                continue

        if Client.connected == False:
            Client.client_socket.close()

def broadcast(message):
    message = ""
    for client in client_list.values():
        client.send(message.encode(FORMAT))

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:    
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started listening on {HOST}:{PORT} for client connection...")
    except:
        print("Server failed to start, try again!")
        # server.shutdown(socket.SHUT_RDWR)
        server.close()

    while True:
        Client.client_socket, Client.client_addr = server.accept()
        
        with Client.client_socket:
            thread = threading.Thread(target=Client.handle_client, args=(Client.client_socket, Client.client_addr))
            thread.start()
            print(f"Current active connections: {threading.active_count() -1}")

    server.shutdown(socket.SHUT_RDWR)
    server.close()

def main():
    run_server()

if __name__ == '__main__':
    main()

