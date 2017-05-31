import argparse
import socket
import random
import sys


MAX_BYTES = 655355


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() > 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)


def client(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    # instead of having to use sock.sendto() all the time, which
    # requires an explicit address tuple, we can use connect() and send().
    # Also prevents client promiscuity by setting UDP preferred destination;
    # OS will discard any incoming packets whose return address does not
    # match the connected address. Not a form of security!
    sock.connect((hostname, port))  # can only connect to one server at a time
    print('Client socket name is {}'.format(sock.getsockname()))

    delay = 0.1  # in seconds
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)  # no address tuple, just data here!
        print('Waiting up to {} for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout:
            delay *= 2  # wait longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down')
        else:
            break

    print('The server says {!r}'.format(data.decode('ascii')))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to play')
    # call with "" to act as a wildcard and accept from 0.0.0.0
    parser.add_argument('host', help='interface the server listens at;'
                        'host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]  # closure - binds either server or client to function
    function(args.host, args.p)  # invokes bound function with port
