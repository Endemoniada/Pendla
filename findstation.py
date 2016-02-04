# coding=utf-8

# TO-DO
#
# - Take input for search
# - Format search URL and fetch results
# - Parse results and allow user to choose one

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, quote
import json


def get_search_string():
    string = raw_input("Sök efter hållplats: ")
    print
    return string


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
        print "Resultat:"
        for r in data['ResponseData']:
            print r['SiteId'] + " " + r['Name']

if __name__ == '__main__':
    main()
