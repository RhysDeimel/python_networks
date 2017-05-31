import argparse
import socket
from datetime import datetime


MAX_BYTES = 65535


def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('Listening at {}'.format(sock.getsockname()))  # returns socket own address
    while True:
        data, address = sock.recvfrom(MAX_BYTES)  # like recv but returns address as well
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = 'The time is {}'.format(datetime.now())
    print("Sending '{}' to server ('127.0.0.1', {})".format(text, port))
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port))
    print('The OS assigned me the address {}'.format(sock.getsockname()))  # gets client IP
    # Below is dangerous because it's not checking if response came from server
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print('The server {} replied {!r}'.format(address, text))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]  # closure - binds either server or client to function
    function(args.p)  # invokes bound function with port
