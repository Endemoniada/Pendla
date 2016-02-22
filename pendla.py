#!/usr/bin/python
# coding=utf-8

"""Pendla v1.2.0 - Hjälper dig hinna hem!

Usage:
    pendla.py
    pendla.py <station name> <lines>... [-l | --loop]
    pendla.py [-l | --loop]
    pendla.py -h | --help | -V | --version

Options:
    -h --help               Show this screen.
    -V --version            Show version.
    -l --loop               Loop program once every minute.

"""

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, URLError, HTTPError
import json
import os
from datetime import datetime
from lib.docopt import docopt
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

    def print_site(self):
        print
        print color.DARKCYAN + color.BOLD + self.site_name + color.END

    def print_departures(self):
        i = 0
        u = 0

        for t in self.traffic_types:
            for d in self.api_data['ResponseData'][t]:
                now = int(time())
                try:
                    tt_unix = self.get_unix_time(d['TimeTabledDateTime'])
                    ex_unix = self.get_unix_time(d['ExpectedDateTime'])
                    tt_string = self.get_string_time(d['TimeTabledDateTime'])
                    ex_string = self.get_string_time(d['ExpectedDateTime'])
                except:
                    pass
                if self.quicksearch:
                    if d['LineNumber'] in self.lines:
                        u += 1
                    else:
                        continue

                    if i > 9:
                        break
                else:
                    if int(d['LineNumber']) in self.lines and self.lines[int(d['LineNumber'])] == d['Destination']:
                        u += 1
                    else:
                        continue

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
        if u == 0:
            print "Inga avgångar matchade din sökning."

    def __init__(self, quicksearch=False):
        self.traffic_types = ["Metros", "Buses", "Trains", "Trams", "Ships"]
        self.quicksearch = quicksearch
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
def get_api_json_data(site_id):
    url = "http://endemoniada.org/trafiklab.php?api=realtimedepartures" + \
          "&siteid=" + str(site_id) + "&timewindow=60"
    stream = urlopen(url)
    data = json.load(stream)
    if data['StatusCode'] != 0:
        try:
            raise APIError(data['StatusCode'], data['Message'])
        except APIError as e:
            print "StatusCode: %s\nMessage: %s" % (
                e.code, e.message
            )
    return data


def print_header(quicksearch=False):
    """Print a pretty header before outputing stations and departures"""
    if not quicksearch:
        print color.GREEN + color.BOLD + '%-8s' % "Gå om",
    print color.GREEN + color.BOLD + '%-8s' % "Avgång",
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


class Stations(object):
    """docstring for Stations

    Class describing a set of stations with functions to fetch and print
    their data in a simple fashion.
    """

    def __init__(self, config, quicksearch=False):
        self.stations = {}
        self.config = config
        self.quicksearch = quicksearch

    def populate_stations(self):
        for k, v in self.config.iteritems():
            self.stations[k] = Station()
            self.stations[k].site_name = v['site_name']
            self.stations[k].distance = v['distance']
            self.stations[k].lines = v['lines']

    def get_stations(self):
        while True:
            os.system('clear')
            print_header(quicksearch)
            # Loop through all stations and:
            # (1) fetch data from API
            # (2) print relevant departures
            for s, o in self.stations.iteritems():
                o.print_site()
                try:
                    o.api_data = get_api_json_data(s)
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
            if loop:
                sleep(looptime)
            else:
                break


def main(args):
    CONFIG_FILE = "config.yml"
    config = read_config(CONFIG_FILE)

    loop = args['--loop']
    looptime = 60
    quicksearch = False

    qs_name = arguments['<station name>']
    qs_lines = arguments['<lines>']

    stations = {}

    if qs_name:
        quicksearch = True
        import findstation
        os.system('clear')
        result = findstation.main(None, qs_name)
        for k, v in result.iteritems():
            stations[k] = Station(True)
            stations[k].site_name = v
            stations[k].lines = qs_lines
            break
    else:
        for k, v in config.iteritems():
            stations[k] = Station()
            stations[k].site_name = v['site_name']
            stations[k].distance = v['distance']
            stations[k].lines = v['lines']

    while True:
        os.system('clear')
        print_header(quicksearch)
        # Loop through all stations and:
        # (1) fetch data from API
        # (2) print relevant departures
        for s, o in stations.iteritems():
            o.print_site()
            try:
                o.api_data = get_api_json_data(s)
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
        if loop:
            sleep(looptime)
        else:
            break

if __name__ == '__main__':
    try:
        arguments = docopt(__doc__, version='Pendla v1.2.0')
        main(arguments)
        exit()
    except KeyboardInterrupt:
        print " Exiting..."
