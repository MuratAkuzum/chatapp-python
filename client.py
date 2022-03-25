import socket, threading

HOST = "127.0.0.1"
PORT = 12345
SIZE = 1024
FORMAT = 'utf-8'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    def receive():
        while True:
            data_receive = server.recv(SIZE).decode(FORMAT)
            print(f"Server sends: {data_receive}")

    def send():
        while True:
            data = input("> ")
            server.send(data.encode(FORMAT))
        

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

if __name__ == '__main__':
    main()



    # def send():
    #     while True:
    #         data = input("> ")

    #         if data == "/quit":
    #             print("Closing connection...")
    #             server.close()
    #             return
    #         elif data:
    #             server.send(data.encode(FORMAT))
    #         else:
    #             return    