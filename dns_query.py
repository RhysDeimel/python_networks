#!/usr/bin/env python3

# Basic DNS query
# Prints a sequence of objects that is returned
# name, time in seconds before cache expires, class (IN = internet address),
# type (A, NS, etc), data - to connect or contact a service

import argparse
import dns.resolver


def lookup(name):
    # A = IPv4, AAAA = IPv6, NS = name server, MX = mail server,
    # CNAME = canonical name - is alias for another domain
    qtype = ['A', 'AAAA', 'CNAME', 'MX', 'NS']

    for el in qtype:
        answer = dns.resolver.query(name, el, raise_on_no_answer=False)
        if answer.rrset is not None:
            print(answer.rrset)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resolve a name using DNS')
    parser.add_argument('name', help='name that you want to look up in DNS')
    lookup(parser.parse_args().name)
