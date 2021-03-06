#!/usr/bin/python

__description__  = 'Quickly hacked together script to query cymon.io for a' \
                   'single ip record from a Splunk custom command. Recommended'\
                   'to use with Dynamic drilldowns'
__requirements__ = 'Splunk'
__author__       = 'xg5-simon'
__email__        = 'simonlvgn at gmail com'
__version__      = '0.0.2 alpha'
__date__         = '13/01/2016'


import re
import collections
import json
import csv
import sys
import string
import requests
import time
import socket

import splunk.Intersplunk


API_KEY = ''
HTTP_PROXY  = ''
HTTPS_PROXY = ''


class cymon(object):

    def __init__(self, auth_token=None,
        endpoint = 'https://cymon.io/api/nexus/v1'):
        self.endpoint = endpoint
        self.session = requests.Session()
        self.session.headers = {'content-type': 'application/json',
                                'accept': 'application/json'}
        self.session.proxies = {
            "http":  HTTP_PROXY,
            "https": HTTPS_PROXY,
        }
        if auth_token:
            self.session.headers.update({'Authorization': 'Token {0}'.format(auth_token)})

    def get(self, method, params=None):
        r = self.session.get(self.endpoint + method, params=params, proxies=self.session.proxies)
        r.raise_for_status()
        json = r.content
                #print json
        return json

    def ip_lookup(self, ip_addr):
        r = self.get('/ip/' + ip_addr + '/events')
        return r

    def domain_lookup(self, name):
        r = self.get('/domain/' + name)
        return r


def validate_ip(ip_dom):
    ''' Need to add better logic here. If variable passed to this function is
        not a valid ipv4 it "assumes" it is a valid domain.'''
    try:
        socket.inet_aton(ip_dom)
        return True
    except:
        return False


def main():
    (isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)
    if len(sys.argv) < 2:
        splunk.Intersplunk.parseError("No arguments provided, please provide an ip address or URL. E.g, ""| cymon __EXECUTE__ 8.8.8.8 | spath input=cy""")
        sys.exit(0)

    api = cymon(API_KEY)
    search_obj = sys.argv[1]
    query_obj = validate_ip(search_obj)

    if query_obj == True:
        result_json = api.ip_lookup(search_obj)
    else:
        result_json = api.domain_lookup(search_obj)

    output = csv.writer(sys.stdout)
    data = [['cy'],[result_json]]
    output.writerows(data)

main()
