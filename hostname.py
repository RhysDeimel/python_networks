# Hostname resolution example

import socket


hostname = 'www.python.com'
addr = socket.gethostbyname(hostname)
print('The IP address of {} is {}'.format(hostname, addr))
