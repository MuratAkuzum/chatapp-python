import socket, threading

HOST = "127.0.0.1"
PORT = 12344
SIZE = 1024
FORMAT = 'utf-8'

class Channel:
    global channel_list_public 
    channel_list_public = dict()
    # channel_list_private = list()
    def __init__(self, channel_name: str, owner: str, public: bool, members: list()):
        # TODO: Add option to make it public or private after creation:
        self.channel_name = channel_name
        self.owner = owner
        self.public = public
        self.members = members

    def channel_create(channel_name: str, username: str):
        new_channel = Channel(channel_name, username, True, username)

        channel_list_public[new_channel.channel_name] = new_channel.owner

    def channel_join(channel_name:str, username: str):
        if channel_name.public:
            channel_name.members.append(username)
            print(f"{channel_name.members}")

class Client:
    global client_list
    client_list = {}
    def __init__(self, client_socket, client_addr):
        self.username: str = ""
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.connected: bool
        self.channel_member: str

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

    def client_handle(self, client_socket, client_addr) -> None:
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
                try:
                    data_split = data_received.split(" ")
                    channel_command = data_split[1]
                    channel_name = data_split[2]
                except:
                    self.client_socket.send(f"[SERVER]: Invalid command, correct usage: /channel <command> <channel-name>".encode(FORMAT))
                    continue
                
                if channel_command == "create":
                    new_channel = Channel.channel_create(channel_name, self.username)
                    self.client_socket.send(f"[SERVER]: Private Channel named '{channel_name}' has been created!".encode(FORMAT))

                elif channel_command == "join":
                    # TODO: connect the user to the channel if not already a member, if it is public, if not blacklisted, recently kicked
                    if channel_name in channel_list_public.keys():
                        new_channel.channel_join(channel_name, self.username)
                        print(f"{new_channel.members}")

                    # self.client_socket.send(f"[SERVER]: {self.username} has entered the channel {channel_name.channel_name}.".encode(FORMAT))
                    # self.client_socket.send(f"[SERVER]: Failed to join the channel '{channel_name.channel_name}! It either doesn't exist or not public.".encode(FORMAT))
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
                    if data_split[2] == "all":
                        key_id = 1
                        for key, value in channel_list.items():
                            self.client_socket.send(f"{key_id}) Channel '{key}' owned by {value}".encode(FORMAT))
                            key_id += 1
                    elif data_split[2] in channel_list.items():
                        self.client_socket.send(f"{data_split[2]} ".encode(FORMAT))
                    elif data_split[2] not in channel_list.keys():
                        self.client_socket.send(f"{data_split[2]} does not exist or is private!".encode(FORMAT))
                    
                    else:
                        self.client_socket.send(f"[SERVER]: Invalid command, correct usage: /channel who <channel-name> or <all> for all channels".encode(FORMAT))

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
        thread = threading.Thread(target=new_client.client_handle, args=(new_client.client_socket, new_client.client_addr), daemon=True)
        thread.start()
        print(f"Current active connections: {threading.active_count() -1}")

    server.shutdown(socket.SHUT_RDWR)
    server.close()

if __name__ == '__main__':
    main()

