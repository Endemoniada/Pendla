#!/usr/bin/python
# coding=utf-8

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, quote
import json


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


def print_search_results(results):
    """Print a pretty header before outputing search results"""
    print color.GREEN+color.BOLD+'%-4s' % "ID",
    print "Namn",
    print color.END

    for r in results:
        print color.DARKCYAN + r['SiteId'] + color.YELLOW + " " + r['Name'],
        print color.END


def main():
    API_KEY = "e24b05ad190347b3aa55284738027712"

    # api.sl.se/api2/typeahead.json?key=e24b05ad190347b3aa55284738027712&searchstring=Helenelund&stationsonly=True&maxresults=10

    search_string = get_search_string()
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
        print_search_results(data['ResponseData'])

if __name__ == '__main__':
    main()
