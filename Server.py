import socket
from threading import Thread, Event

class Server:
    def __init__(self, serverHost='localhost', serverPort=9999):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.shutdown_event = Event()  # Shared shutdown flag

    def handle_client(self, client_socket, client_address):
        print(f'Connection from {client_address} established')
        try:
            client_socket.send(b"Welcome to Server... Type 'exit' to disconnect.\n")

            while not self.shutdown_event.is_set():
                # Receive a message from the client
                client_message = client_socket.recv(1024).decode('utf-8')
                if not client_message:
                    break  # Client closed the connection
                print(f"Client {client_address} says: {client_message}")

                if client_message.lower() == "exit":
                    print(f"Client {client_address} requested server shutdown.")
                    self.shutdown_event.set()  # Signal to stop the server
                    break

                # Send a response back to the client
                server_message = f"Message received: {client_message}"
                client_socket.send(server_message.encode('utf-8'))

        except Exception as e:
            print(f"Error with client {client_address}: {e}")

        finally:
            client_socket.close()
            print(f"Connection with {client_address} closed.")

    def main(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            connection.bind((self.serverHost, self.serverPort))
            connection.listen(5)
            print(f"Server started on {self.serverHost}:{self.serverPort}")

            while not self.shutdown_event.is_set():
                # Accept new client connections
                try:
                    connection.settimeout(1)  # Non-blocking accept with timeout
                    client_socket, client_address = connection.accept()
                    client_thread = Thread(target=self.handle_client, args=(client_socket, client_address))
                    client_thread.start()
                except socket.timeout:
                    continue  # Allow periodic checks for shutdown event

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            connection.close()
            print("Server shutting down... Goodbye!")

if __name__ == "__main__":
    host = input("Enter server host (default 'localhost'): ") or 'localhost'
    port = input("Enter server port (default 9999): ") or 9999
    server = Server(serverHost=host, serverPort=int(port))
    server.main()