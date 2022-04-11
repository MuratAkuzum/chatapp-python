use std::{io::{BufReader, BufRead, Write}, collections::{HashMap}, net::{TcpListener, TcpStream, SocketAddr, Shutdown}, thread};

const SOCKET: &str = "127.0.0.1:8080";

fn main() {

    // Initializing a socket/address for the server to: 
    let listener = TcpListener::bind(SOCKET).expect("!! Could not bind socket!");
    println!("[SERVER]: Server has been started on {}", SOCKET);

    // Listening for and accept client connections: 
    for client_connection in listener.incoming() {
        // let mut clients = HashMap::new();
        
        match client_connection {
            // If connection is successful, print the info and create a thread for the connection: 
            Ok(client_connection) => {
                
                let new_client = Client::client_login(client_connection);
                // clients.insert(new_client.username, new_client.client_connection);
                thread::spawn(move || {Client::handle_client(new_client.username, new_client.client_connection)});
            }
            // If connection fails, print the info: 
            Err(err) => {println!("Connection has failed due to error: {}", err)}
        }
    }
}


struct Client {
    username: String,
    client_connection: TcpStream,
    connected: bool,
}

impl Client {
    fn client_login(client_connection: TcpStream) -> Client {
        let client_connection_clone = client_connection.try_clone().unwrap();
        // Creating a buffer to hold data received from the client: 
        let mut data_receive = BufReader::new(client_connection);

        // Accepting the first data received as username for the client: 
        let mut username_buffer = String::new();
        data_receive.read_line(&mut username_buffer).unwrap();
        let username = username_buffer.trim().to_lowercase();

        Client {
            username: username,
            client_connection: client_connection_clone,
            connected: true
        }
    }

    fn client_logoff(username: String) {
        
        println!("[SERVER]: {} has just left the server!", username);

    }
    
    // Function to handle each connected client: 
    fn handle_client(username: String, client_connection: TcpStream) {
        println!("[SERVER]: Connection has been accepted from {:?}", client_connection.peer_addr().unwrap());

        // Creating a buffer to hold data received from the client: 
        let mut data_receive = BufReader::new(client_connection);
        
        // Creating a loop to keep listening for data sent by the client: 
        loop {
            // Buffer to hold the converted data into string: 
            let mut data_buffer = String::new();

            // Breaking out of loop if the client stops sending data: 
            if data_receive.read_line(&mut data_buffer).is_err() {
                Client::client_logoff(username);
                break;
            }

            // Writing the data received from client into string buffer and printing it: 
            data_receive.get_ref().write(data_buffer.as_bytes()).unwrap();
            println!("[SERVER]: {}: {}", username, data_buffer.trim());
        }
    }

    
}


