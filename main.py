# coding=utf-8

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
from datetime import datetime, date
from time import mktime, time

try:
    import yaml
except ImportError:
    print "Requires PyYAML module to function"
    exit()


class Station(object):
    """docstring for Station

    Class describing a station of a particular traffic type,
    with different stops and lines as well as a time it
    takes to walk to it.
    """


    def print_departures(self):
        print
        print color.DARKCYAN + color.BOLD + self.station_name + color.END
        i = 0
        for d in self.api_data['ResponseData'][self.traffic_type]:
            currEpochTime = int(time())
            timeTableEpoch = int(mktime(datetime.strptime(d['TimeTabledDateTime'], "%Y-%m-%dT%H:%M:%S").timetuple()))
            expectedEpoch = int(mktime(datetime.strptime(d['ExpectedDateTime'], "%Y-%m-%dT%H:%M:%S").timetuple()))
            timeTablePretty = datetime.strftime(datetime.strptime(d['TimeTabledDateTime'], "%Y-%m-%dT%H:%M:%S"), "%H:%M")
            ExpectedPretty = datetime.strftime(datetime.strptime(d['ExpectedDateTime'], "%Y-%m-%dT%H:%M:%S"), "%H:%M")

            if i >= 3:
                break

            if (timeTableEpoch-currEpochTime) < self.distance * 60:
                continue

            # print color.YELLOW + '%-7s' % "X min" + color.END,
            # print color.END + getLeaveTime(self.distance * 60, currEpochTime, expectedEpoch),
            print color.END + remaining_time(self.distance, expectedEpoch),
            print color.YELLOW + '%-7s' % d['DisplayTime'] + color.END,
            if timeTableEpoch == expectedEpoch:
                # Visa tabelltid
                print '%-11s' % timeTablePretty,
            # ...Annars printa både tabelltid samt ny tid
            else:
                # Visa tabelltid
                print '%-11s' % (timeTablePretty+"/"+color.RED+ExpectedPretty+color.END),
            # print color.DARKCYAN+'%-3s' % d['LineNumber'],
            print '%-11s' % (color.DARKCYAN + d['LineNumber'] + " " + color.YELLOW + d['Destination']) + color.END
            if d['Deviations']:
                print color.DARKCYAN + "- " + d['Deviations'][0]['Text'][:80] + color.END
            i += 1

    def __init__(self):
        self.station_id = None
        self.station_name = None
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
def get_api_json_data(api_key, station_id):
    url = "http://api.sl.se/api2/realtimedepartures.json?key=" + \
            str(api_key) + "&siteid=" + str(station_id) + "&timewindow=60"
    stream = urlopen(url)
    data = json.load(stream)
    if data['StatusCode'] != 0:
        print "StatusCode: %s\nMessage: %s" % (
            data['StatusCode'], data['Message']
        )
        exit()
    return data

def print_header():
        """Print a pretty header before outputing stations and departures"""
        print color.GREEN+color.BOLD+'%-8s' % "Gå om",
        print '%-8s' % "Avgång",
        print '%-11s' % "Tid",
        print "Destination",
        print color.END

# WIP
# To be finished properly later. This is currently
# calculated inside the Station class
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
        stations[k].station_id = v['station_id']
        stations[k].station_name = v['station_name']
        stations[k].distance = v['distance']
        stations[k].lines = v['lines']
        stations[k].traffic_type = v['traffic_type']

    print_header()

    # Loop through all stations and:
    # (1) fetch data from API
    # (2) print relevant departures
    for s, o in stations.iteritems():
        o.api_data = get_api_json_data(API_KEY, o.station_id)
        o.print_departures()

if __name__ == '__main__':
    main()
