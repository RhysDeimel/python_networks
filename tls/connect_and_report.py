#!/usr/bin/env python3
# Attempt a TLS connection and, if successful, report its properties

import argparse
import socket
import ssl
import sys
import textwrap
import ctypes
from pprint import pprint

def open_tls(context, address, server=False):
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if server:
        raw_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        raw_sock.bind(address)
        raw_sock.listen(1)
        say('Interface where we are listening', address)
        raw_client_sock, address = raw_sock.accept()
        return context.wrap_socket(raw_client_sock, server_side=True)
    else:
        say('Address we want to talk to', address)
        raw_sock.connect(address)
        return context.wrap_socket(raw_sock)

def describe(ssl_sock, hostname, server=False, debug=False):
    cert = ssl_sock.getpeercert()
    if cert is None:
        say('Peer certificate', 'none')
    else:
        say('Peer certificate', 'provided')
        subject = cert.get('subject', [])
        names = [name for names in subject for (key, name) in names
                 if key == 'commonName']
        if 'subjectAltName' in cert:
            names.extend(name for (key, name) in cert['subjectAltName']
                         if key == 'DNS')

        say('Name(s) on peer certificate', *names or ['none'])
        if (not server) and names:
            try:
                ssl.match_hostname(cert, hostname)
            except ssl.CertificateError as e:
                message = str(e)
            else:
                message = 'Yes'
            say('Whether name(s) match the hostname', message)
        for category, count in sorted(context.cert_store_stats().items()):
            say('Certificates loaded of type {}'.format(category), count)

    try:
        protocol_version = SSL_get_version(ssl_sock)
    except Exception:
        if debug:
            raise
    else:
        say('Protocol version negotiated', protocol_version)

    cipher, version, bits = ssl_sock.cipher()
    compression = ssl_sock.compression()

    say('Cipher chosen for this connection', cipher)
    say('Cipher defined in this version', version)
    say('Cipher key has this many bits', bits)
    say('Compression algorithm in use', compression or 'none')

    return cert


class PySSLSocket(ctypes.Structure):
    """Reach behind the scenes for a socket's TLS protocol version."""

    lib = ctypes.CDLL(ssl._ssl.__file__)
    lib.SSL_get_version.restype = ctypes.c_char_p
    address = id(ssl_sock._sslobj)
    struct = ctypes.cast(address, ctypes.POINTER(PySSLSocket)).contents
    version_bytestring = lib.SSL_get_version(struct.ssl)
    return version_bytestring.decode('ascii')




























