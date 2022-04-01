import socket, threading, sys

HOST = "127.0.0.1"
PORT = 12345
SIZE = 1024
FORMAT = 'utf-8'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    def send():
        while True:
            try:
                data = input("")
                server.send(data.encode(FORMAT))
            except KeyboardInterrupt:
                server.close()
                sys.exit()

    def receive():
        while True:
            try: 
                data_receive = server.recv(SIZE).decode(FORMAT)
                if len(data_receive) == 0:
                    server.shutdown(socket.SHUT_RDWR)
                    server.close()
                    break
                print(f"{data_receive}")
            except:
                break

        sys.exit()

    send_thread = threading.Thread(target=send, daemon=True)
    send_thread.start()
    
    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    receive()

    server.shutdown(socket.SHUT_RDWR)
    server.close()
    sys.exit()

if __name__ == '__main__':
    main()

