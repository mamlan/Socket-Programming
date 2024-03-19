import socket

## function to create a server
def create_server_socket(port=8000):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    return server_socket

#manage incoming clients
def handle_client_connection(client_socket):
    request_data = client_socket.recv(2048)
    #get the url as it is important
    requested_url = request_data.split()[1].decode('utf-8')[1:]
    cache_file_name = requested_url.replace('www.', '', 1).replace('/', '_')
    host_name = requested_url.split('/')[0].replace('www.', '', 1)
    resource_path = '/'.join(requested_url.split('/')[1:])

    try:
        with open(cache_file_name, 'r') as cache_file:
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + cache_file.read().encode())
            print('Served from cache: ', cache_file_name)
    except FileNotFoundError:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
                remote_host_ip = socket.gethostbyname(host_name)
                remote_socket.connect((remote_host_ip, 80))
                http_request = f"GET /{resource_path} HTTP/1.1\r\nHost: {host_name}\r\nConnection: close\r\n\r\n"
                remote_socket.sendall(http_request.encode())

                response_data = remote_socket.recv(8192)
                with open(cache_file_name, "wb") as cache_file:
                    cache_file.write(response_data)

                client_socket.sendall(response_data)
                print('Fetched from the web and cached: ', cache_file_name)
        except IOError:
            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n")


def start_server(port=8000):
    server_socket = create_server_socket(port)
    print("Server is ready to serve on port", port)

    try:
        while True:
            client_socket, _ = server_socket.accept()
            print("Accepted new connection")
            handle_client_connection(client_socket)
            client_socket.close()
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
