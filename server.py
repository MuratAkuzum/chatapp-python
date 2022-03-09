import socket, threading

HOST = "127.0.0.1"
PORT = 8888
SIZE = 1024
FORMAT = 'utf-8'

# /send <username>
# /who <username>


def handle_client(client_socket, client_addr):
    print(f"New client connected with {client_addr}!")
    client_socket.send("Welcome to the server!".encode(FORMAT))

    data_received = client_socket.recv(SIZE).decode(FORMAT)
    print(f"{client_addr} sends: {data_received}")





def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen(5)
    print(f"Server is started on {HOST}:{PORT}")
    print(f"Waiting for client connection...")
    

    while True:
        client_socket, client_addr = server.accept()


        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()


    server.close()

if __name__ == '__main__':
    main()



