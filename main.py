#!/usr/bin/python
# coding=utf-8

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, URLError, HTTPError
import json
import os
from datetime import datetime
from time import mktime, time, sleep

try:
    import yaml
except ImportError:
    print "Requires PyYAML module to function"
    exit()


class APIError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return repr({self.code: self.message})


class Station(object):
    """docstring for Station

    Class describing a station of a particular traffic type,
    with different stops and lines as well as a time it
    takes to walk to it.
    """

    def get_unix_time(self, string):
        return int(mktime(datetime.strptime(string, "%Y-%m-%dT%H:%M:%S").timetuple()))

    def get_string_time(self, unix):
        return datetime.strftime(datetime.strptime(unix, "%Y-%m-%dT%H:%M:%S"), "%H:%M")

    def print_departures(self):
        print
        print color.DARKCYAN + color.BOLD + self.site_name + color.END

        i = 0

        for d in self.api_data['ResponseData'][self.traffic_type]:
            if int(d['LineNumber']) in self.lines and self.lines[int(d['LineNumber'])] == d['Destination']:
                pass
            else:
                continue
            now = int(time())
            tt_unix = self.get_unix_time(d['TimeTabledDateTime'])
            ex_unix = self.get_unix_time(d['ExpectedDateTime'])
            tt_string = self.get_string_time(d['TimeTabledDateTime'])
            ex_string = self.get_string_time(d['ExpectedDateTime'])

            if i > 1:
                break

            if (tt_unix - now) < self.distance * 60:
                continue

            print color.END + remaining_time(self.distance, ex_unix),
            print color.YELLOW + '%-7s' % d['DisplayTime'] + color.END,
            if tt_unix == ex_unix:
                print '%-11s' % tt_string,
            else:
                print '%-11s' % (tt_string+"/"+color.RED+ex_string+color.END),
            print '%-11s' % (color.DARKCYAN + d['LineNumber'] + " " + color.YELLOW + d['Destination']) + color.END
            if d['Deviations']:
                print color.DARKCYAN + "- " + d['Deviations'][0]['Text'][:80] + color.END

            i += 1

    def __init__(self):
        self.site_name = None
        # Walking distance as time in minutes, default 5
        self.distance = 5
        self.traffic_type = None
        self.lines = {}
        self.api_data = None
        self.departures = None


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


# Fetch the data from Trafiklab API and check for
# common errors.
def get_api_json_data(api_key, site_id):
    url = "http://api.sl.se/api2/realtimedepartures.json?key=" + \
            api_key + "&siteid=" + str(site_id) + "&timewindow=60"
    stream = urlopen(url)
    data = json.load(stream)
    if data['StatusCode'] != 0:
        try:
            raise APIError(data['StatusCode'], data['Message'])
        except APIError as e:
            print "StatusCode: %s\nMessage: %s" % (
                e.code, e.message
            )
        # if data['StatusCode'] == 1002:
        #     print "API key is invalid or wrong."
        # else:
        #     print "StatusCode: %s\nMessage: %s" % (
        #         data['StatusCode'], data['Message']
        #     )
        # exit()
    return data


def print_header():
        """Print a pretty header before outputing stations and departures"""
        print color.GREEN+color.BOLD+'%-8s' % "Gå om",
        print '%-8s' % "Avgång",
        print '%-11s' % "Tid",
        print "Destination",
        print color.END


def remaining_time(distance, departure):
    """Take walking time (in minutes) and departure time (as string)
    and return a string with minutes remaining or "now!" if minutes
    equal 0.
    """
    now = int(time())

    remaining_seconds = (departure - now) - (distance * 60)
    remaining_minutes = int(float(remaining_seconds) / 60.0)

    if remaining_minutes <= 0:
        return color.BOLD + color.RED + '%-7s' % "Nu!" + color.END
    elif remaining_minutes <= 5:
        return color.BOLD + color.YELLOW + '%-7s' % (str(remaining_minutes)+" min") + color.END
    else:
        return color.YELLOW + '%-7s' % (str(remaining_minutes)+" min") + color.END


def read_config(config_file):
    try:
        with open(config_file, 'r') as stream:
            # läser config.yml och skapar en dict 'cfg' med alla värden
            config_data = yaml.load(stream)
            return config_data
    except IOError:
        print "No configuration file found!"
        raise


def main():
    API_KEY = "72e87e92af514d73830ba8cf89b8197d"
    CONFIG_FILE = "config.yml"

    stations = {}

    for k, v in read_config(CONFIG_FILE).iteritems():
        stations[k] = Station()
        stations[k].site_name = v['site_name']
        stations[k].distance = v['distance']
        stations[k].lines = v['lines']
        stations[k].traffic_type = v['traffic_type']

    while True:
        os.system('clear')
        print_header()
        # Loop through all stations and:
        # (1) fetch data from API
        # (2) print relevant departures
        for s, o in stations.iteritems():
            try:
                o.api_data = get_api_json_data(API_KEY, s)
            except HTTPError, e:
                print "HTTP error: " + str(e.code)
            except URLError:
                print "Network error"
            except APIError as e:
                print "StatusCode: %s\nMessage: %s" % (
                    e.code, e.message
                )
            else:
                o.print_departures()
        sleep(60)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print " Exiting..."
