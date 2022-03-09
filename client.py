import socket

HOST = "127.0.0.1"
PORT = 8888
SIZE = 1024
FORMAT = 'utf-8'

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))

    while True:
        
        data = input(">")
        data_sent = server.send(data.encode(FORMAT))

    server.close()

if __name__ == '__main__':
    main()