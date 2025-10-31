import socket

def start_udp_server(port=8080):
    """A simple UDP echo server that replies with 'ack'."""
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', port))
    print(f"UDP server running on port {port} (Ctrl+C to stop)")

    try:
        while True:
            data, addr = server.recvfrom(4096)
            print(f"Received from {addr}: {data.decode(errors='ignore')}")
            if data:
                server.sendto(b'ack', addr)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    start_udp_server()
