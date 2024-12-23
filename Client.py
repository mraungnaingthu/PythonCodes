import socket

class Client:
    def __init__(self, serverHost='localhost', serverPort=9999):
        self.serverHost = serverHost
        self.serverPort = serverPort

    def main(self):
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Connect to the server
            print(f"Attempting to connect to server at {self.serverHost}:{self.serverPort}...")
            client_socket.connect((self.serverHost, self.serverPort))
            print("=" * 50)
            print(f"Connected to server at {self.serverHost}:{self.serverPort}")
            print("Type 'exit' to close the connection and stop the server.")
            print("=" * 50)

            while True:
                # Receive a message from the server
                try:
                    server_message = client_socket.recv(1024).decode('utf-8')
                    if not server_message:
                        print("Server closed the connection.")
                        break
                    print(f"Server says: {server_message}")
                except socket.timeout:
                    print("Timeout while waiting for server response.")
                    break

                # Get user input to send to the server
                client_message = input("Enter your message to send to the server: ")

                # Send the user's message to the server
                client_socket.sendall(client_message.encode('utf-8'))

                if client_message.lower() == "exit":
                    print("Exiting... Shutting down server and client.")
                    break

        except ConnectionRefusedError:
            print(f"Unable to connect to the server at {self.serverHost}:{self.serverPort}. Please try again later.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the socket
            client_socket.close()
            print("Connection closed.")

if __name__ == "__main__":
    # Allow dynamic server configuration
    host = input("Enter server host (default 'localhost'): ") or 'localhost'
    port = input("Enter server port (default 9999): ") or 9999

    client = Client(serverHost=host, serverPort=int(port))
    client.main()