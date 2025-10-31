import argparse
import re
import socket

def scan_udp(host, start, end):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            try:
                s.sendto(b'test', (host, port))
                s.recvfrom(1024)
                print(f'Port {port} is open')
            except (socket.timeout, socket.error):
                print(f'Port {port} is closed')

def scan_tcp(host, start, end):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            try:
                s.connect((host, port))
                print(f'Port {port} is open')
            except (socket.timeout, socket.error):
                print(f'Port {port} is closed')

def parse_ports(port_str):
    if port_str.isdigit():
        return int(port_str), int(port_str)
    m = re.match(r'^(\d+)-(\d+)$', port_str)
    if m:
        a, b = int(m[1]), int(m[2])
        if a <= b:
            return a, b
    print('Invalid port number(s)')
    exit(1)

def main():
    parser = argparse.ArgumentParser(usage="tinyscanner [OPTIONS] [HOST] [PORT]", add_help=False)
    parser.add_argument('-p', required=True, help='Range of ports to scan')
    parser.add_argument('-u', help='UDP scan (host)')
    parser.add_argument('-t', help='TCP scan (host)')
    parser.add_argument('--help', action='help', help='Show this message and exit.')
    args = parser.parse_args()

    if not (args.u or args.t):
        print('Specify either UDP (-u) or TCP (-t)')
        return

    start, end = parse_ports(args.p)
    if args.u:
        scan_udp(args.u, start, end)
    if args.t:
        scan_tcp(args.t, start, end)

if __name__ == "__main__":
    main()