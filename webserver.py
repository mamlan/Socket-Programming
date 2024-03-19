import socket

def initialize_server(port=8888):
    """Initializes and returns a socket object configured to listen on the specified port."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    return server_socket

def serve_client(connection, address):
    """Handles a single client connection, serving requested files or a 404 error."""
    print(f"Connection from {address} has been established.")
    try:
        request = connection.recv(1024)
        requested_file_path = request.split()[1]
        with open(requested_file_path[1:], 'r') as requested_file:
            connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n" + requested_file.read().encode())
            print('Successfully served the requested file to the client.')
    except IOError:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        print('Requested file not found, sent 404 response.')
    finally:
        connection.close()

def run_server(port=8888):
    """Runs the server indefinitely, accepting and serving client connections."""
    server_socket = initialize_server(port)
    print(f"Server is ready to receive connections on port {port}.")

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            serve_client(client_connection, client_address)
    finally:
        server_socket.close()

if __name__ == '__main__':
    run_server()
