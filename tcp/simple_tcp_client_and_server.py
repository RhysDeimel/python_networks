# Simple TCP client and server that sends and receives 16 octets

import argparse
import socket


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('Was expecting {} bytes but only received'
                           ' {} bytes before the socket closed'.format(length, len(data)))
        data += more
    return data


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)  # once listen is called, the socket claimed by bind() will not be used to send and receive data
    # instead, accept() returns a new socket object (and new port) through which communication will occur
    print('Listening at {}'.format(sock.getsockname()))
    while True:
        sc, sockname = sock.accept()  # sc is a new socket object usable to send and receive data
        print('We have accepted a connection from {}'.format(sockname))
        print('\tSocket name:', sc.getsockname())  # local socket
        print('\tSocket peer:', sc.getpeername())  # remote client socket
        message = recvall(sc, 16)
        print('Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print('\tReply sent, socket closed')


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
