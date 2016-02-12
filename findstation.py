#!/usr/bin/python
# coding=utf-8

"""Pendla FindStation v1.1.0 - Hjälper dig hitta stationen att hinna hem ifrån!

Usage:
    findstation.py
    findstation.py <station name>
    findstation.py -h | --help | -V | --version

Options:
    -h --help               Show this screen.
    -V --version            Show version.

"""

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, quote
import json
import os
from lib.docopt import docopt


class color:
    """Establish bash terminal color codes using common names"""
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    LIGHTRED = '\033[1;31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def get_search_string():
    string = raw_input("Sök efter hållplats: ")
    print
    return string


def print_search_results(results, choice=False):
    """Print a pretty header before outputing search results"""
    if choice:
        print color.GREEN + color.BOLD + '%9s' % "ID  ",
    else:
        print color.GREEN + color.BOLD + '%-4s' % "ID  ",
    print "Namn" + color.END

    choices = {}

    i = 1
    for r in results:
        choices[i] = {r['SiteId']: r['Name']}
        if choice: print '%-4s' % ("#" + str(i)),; i += 1
        print color.DARKCYAN + r['SiteId'] + color.YELLOW + " " + r['Name'],
        print color.END

    if choice:
        print
        choice = raw_input("Välj hållplats: ")
        if int(choice) in choices:
            return choices[int(choice)]
        else:
            os.system('clear')
            print "Var vänlig ange ett giltigt nummer.\n"
            return print_search_results(results, True)
    return False


def main(arguments=None, search_string=None):
    API_KEY = "e24b05ad190347b3aa55284738027712"
    choice = False

    # api.sl.se/api2/typeahead.json?key=e24b05ad190347b3aa55284738027712&searchstring=Helenelund&stationsonly=True&maxresults=10

    if arguments and arguments['<station name>']:
        search_string = arguments['<station name>']
    else:
        if not search_string:
            search_string = get_search_string()
        else:
            choice = True
    stations_only = "True"
    max_results = "10"

    url = "http://api.sl.se/api2/typeahead.json?key=" + API_KEY + \
        "&searchstring=" + quote(search_string) + \
        "&stationsonly=" + stations_only + \
        "&maxresults=" + max_results
    stream = urlopen(url)
    data = json.load(stream)

    if data['StatusCode'] != 0:
        print "StatusCode: %s\nMessage: %s" % (
            data['StatusCode'], data['Message']
        )
    else:
        choice = print_search_results(data['ResponseData'], choice)

    if choice:
        return choice

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Pendla v1.1.0')
    try:
        main(arguments)
    except KeyboardInterrupt:
        print "\nExiting..."
    exit()
