# Returns port number of commonly used ports by service name
import socket

# Ports 0-1023 - system or well-known ports
# Ports 1024-49151 - user or registered ports
# Ports >49151 - dynamic / private ports

# database of well-known service names and port numbers usually kept in
# /etc/servics on Linux and Mac OS X machines

print(socket.getservbyname('domain'))  # port 53
print(socket.getservbyname('whois'))  # port 43
print(socket.getservbyname('smtp'))  # port 25
