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
                client_list[Client.username] = Client.client_socket.getpeername()[0]
                print(f"Username: {Client.username} \nAddress: {Client.client_socket.getpeername()[0]}")
                print(f"{client_list}")
                Client.connected = True
                break
            else:
                Client.client_socket.send("Username is already taken, please enter another name:".encode(FORMAT))
                

    def handle_client(client_socket, client_addr):
        print(f"New client connected with {Client.client_socket.getpeername()[0]}!")

        Client.client_login()

        while Client.connected:
            data_received = Client.client_socket.recv(SIZE).decode(FORMAT)
            print(f"{Client.username} sends: {data_received}")

            if len(data_received) == 0:
                print(f"{Client.username} has just left the server!")
                Client.online = False
                Client.connected = False
                client_list.pop(Client.username)
                break
            elif data_received == "/quit":
                print(f"{Client.username} has just left the server!")
                Client.online = False
                Client.connected = False
                client_list.pop(Client.username)
                break
            else:
                pass

        if not Client.connected:
            Client.client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:    
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server started listening on {HOST}:{PORT} for client connection...")
    except:
        server.shutdown(1)
        server.close()
        print("Server failed to start, try again!")
        return 1

    while True:
        Client.client_socket, Client.client_addr = server.accept()
        
        thread = threading.Thread(target=Client.handle_client, args=(Client.client_socket, Client.client_addr))
        thread.start()
        print(f"Current active connections: {threading.active_count() -1}")


# def broadcast(message):
#     message = input("")
#     for client in :
#         client.send(message.encode(FORMAT))

def main():
    run_server()   


if __name__ == '__main__':
    main()



