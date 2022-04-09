import socket, threading

HOST = "127.0.0.1"
PORT = 12345
SIZE = 1024
FORMAT = 'utf-8'

client_list = {}

class Channel:
    def __init__(self):
        self.name: str
        self.members: list[str]
        self.owner: str
        self.co_owners: list[str]

class Client:
    def __init__(self, client_socket, client_addr):
        self.username: str = ""
        self.client_socket = client_socket
        self.client_addr = client_addr
        # connected: bool
        # channel: str

    def client_login(self, client_socket) -> str:
        self.client_socket.send("[SERVER]: Please enter a username to login to the server:".encode(FORMAT))
        while True:
            self.username = self.client_socket.recv(SIZE).decode(FORMAT)
            # TODO: add more filteration while picking a unique username (char limit, allowed special chars etc.)
            if self.username not in client_list.keys():
                client_list[self.username] = self.client_socket
                print(f"Username: {self.username} \nAddress: {self.client_socket.getpeername()[0]}")
                print(f"{client_list}")
                break
            else:
                self.client_socket.send("[SERVER]: Username is already taken, please enter another name:".encode(FORMAT))
        self.client_socket.send(f"[SERVER]: Welcome to the server. You have logged in as {self.username}.\n> Type </help> if you want to see options.".encode(FORMAT))
        return self.username

    def client_logoff(self, username, client_socket) -> None:
        try:
            client_list.pop(self.username, self.client_socket)
            self.client_socket.close()
        except:
            print("Error while trying to log off the client!")


    def handle_client(self, client_socket, client_addr) -> None:
        self.username = self.client_login(self.client_socket)
        print(f"[{self.username}] connected with {self.client_socket.getpeername()[0]}!")

        while True:
            data_received = self.client_socket.recv(SIZE).decode(FORMAT)

            if len(data_received) == 0:
                self.client_socket.send("[SERVER]: Exit request received, closing connection...".encode(FORMAT))
                self.client_logoff(self.username, self.client_socket)
                broadcast(f"[SERVER]: [{self.username}] has just left the server!")
                break
            
            elif data_received == "/quit":
                self.client_socket.send("[SERVER]: Exit request received, closing connection...".encode(FORMAT))
                self.client_logoff(self.username, self.client_socket)
                broadcast(f"[SERVER]: [{self.username}] has just left the server!")
                break

            elif data_received == "/help":
                self.client_socket.send("[SERVER]: choose one of the following commands:\n> Type </quit> if you want to quit the program.\n> Type </send> <username> <your message> to send message to other users.".encode(FORMAT))

            elif data_received == "/who":
                # TODO: Users are not always getting listed always in the same order. Handle /who better.
                # TODO: Add option to search someone specifically : /who murat
                self.client_socket.send(f"[SERVER]: online users:".encode(FORMAT))
                key_id = 1
                for key in client_list.keys():
                    self.client_socket.send(f"{key_id}) {key}".encode(FORMAT))
                    key_id += 1

            elif data_received.startswith("/send"):
                data_split = data_received.split(" ")
                other_username = data_split[1]
                message = data_split[2:]
                if other_username == "server":
                    print(f"[{self.username}]: {' '.join(message)}")
                elif other_username not in client_list.keys():
                    self.client_socket.send("[SERVER]: User is not online or does not exist!".encode(FORMAT))
                else:
                    direct_message(self.username, other_username, ' '.join(message))

            elif data_received.startswith("/channel"):
                data_split = data_received.split(" ")
                channel_name = data_split[1]
                channel_command = data_split[2]
                
                if channel_command == "create":

                    pass
                elif channel_command == "join":
                    # TODO: find the owner and ask permission to join the channel:
                    pass
                elif channel_command == "invite":
                    channel_user = data_split[3]
                    # TODO: invite the user to your channel if exists, if not, create channel if invite is accepted:
                    pass
                elif channel_command == "quit":
                    # TODO: leave channel, if the user is last person in the channel, destroy the channel too:
                    pass
                elif channel_command == "kick":
                    channel_user = data_split[3]
                    # TODO: kick the user if used by the owner of the channel:
                    pass
                elif channel_command == "who":
                    # TODO: list the users in the channel:
                    # TODO: if the username specified, only give information about that user:
                    channel_user = data_split[3]
                    pass
                elif channel_command == "send":
                    # TODO: send message to specified channel name:
                    pass

                else:
                    pass
                    
            else:
                continue

def broadcast(message: str) -> str:
    for client in client_list.values():
        client.send(message.encode(FORMAT))
    print(message)

def direct_message(username, other_username, message) -> None:
    other_client_socket = client_list[other_username]
    other_client_socket.send(f"[{username}] sends: {message}".encode(FORMAT))
    
def main() -> None:
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
        new_client = Client(client_socket, client_addr)
        print(new_client)
        thread = threading.Thread(target=new_client.handle_client, args=(new_client.client_socket, new_client.client_addr), daemon=True)
        thread.start()
        print(f"Current active connections: {threading.active_count() -1}")

    server.shutdown(socket.SHUT_RDWR)
    server.close()

if __name__ == '__main__':
    main()

# TODO: Add more commands for clients to use
# TODO: Remove command log/history from the chat window after done
# TODO: Add timestamps on messages
# TODO: Add more details about the users: online, online since XX:XX, location
# TODO: Add option to save the chat history locally
# TODO: Feature to create chat groups between clients
# TODO: Add option to file transfer

