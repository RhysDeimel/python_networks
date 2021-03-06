# call with: python udp_broadcast.py server ""
#            python udp_broadcast.py server 127.0.0.1
#            python udp_broadcast.py server [external interface]
#            python udp_broadcast.py client [machine hostname]
#            python udp_broadcast.py client [ipaddress of server]
#            python udp_broadcast.py client "<broadcast>"
import argparse
import socket


BUFSIZE = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening for datagrams at {}'.format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print('The client at {} says: {!r}'.format(address, text))


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # the following will broadcast to all servers when client uses broadcast
    # address or "<broadcast>"
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = 'Broadcast datagram!'
    sock.sendto(text.encode('ascii'), (network, port))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' network the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]  # closure - binds either server or client to function
    function(args.host, args.p)  # invokes bound function with port
