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
            print color.END + getLeaveTime(self.distance * 60, currEpochTime, expectedEpoch),
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


# Old function for calculating the "Gå om" message.
# Either pretty this up or replace with remaining_time()
def getLeaveTime(wt, ct, dt):
    # wt=walktime, ct=currtime, dt=departuretime

    # 1. räkna ut sekunder till avgång
    # 2. subtrahera tiden det tar att gå
    # 3. avrunda uppåt till minuter
    # 4. om minuter < 0, skicka "Nu!"

    timeLeftS = (dt - ct) - wt
    # print "timeLeftS="+str(timeLeftS)

    timeLeftM = int(float(timeLeftS) / 60.0)
    # print "TimeLeftM="+str(timeLeftM)

    if timeLeftM <= 0:
        return color.BOLD + color.RED + '%-7s' % "Nu!" + color.END
    if timeLeftM <= 5:
        return color.BOLD + color.YELLOW + '%-7s' % (str(timeLeftM)+" min") + color.END
    return color.YELLOW + '%-7s' % (str(timeLeftM)+" min") + color.END

# Fetch the data from Trafiklab API and check for
# common errors.
def get_api_json_data(api_key, station_id):
    url = "http://api.sl.se/api2/realtimedepartures.json?key=" + \
            api_key + "&siteid=" + station_id + "&timewindow=60"
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

def read_config():
    try:
        with open(CONFIG_FILE, 'r') as stream:
            # läser config.yml och skapar en dict 'cfg' med alla värden
            config_data = yaml.load(stream)
            return config_data
    except IOError:
        print "No configuration file found!"
        raise
    #     print "Creating sample file 'config.yml'. Please edit and save this file before running the program again."
    #     # Skapar en dict med exempel-konfiguration, och skriver denna till en fil
    #     cfg = {}
    #     cfg['pendel'] = {'stationer': [{12345: {'tid': 15, 'linjer': [{123: {'riktning': 1}}, 456]}}]}
    #     cfg['buss'] = {'stationer': [{67890: {'tid': 5, 'linjer': [{12: {'riktning': 2}}]}}]}
    #     with file("config.yml", "w") as stream:
    #         yaml.dump(cfg, stream)

def main():
    API_KEY = "72e87e92af514d73830ba8cf89b8197d"
    CONFIG_FILE = "config.yml"

    # Create a dictionary with each station ID as key,
    # and the Station object as value
    stations = {"9507": Station(),
                "3748": Station()}

    # Set up some values for testing during development
    # These should be removed and replaced by proper config
    stations['9507'].station_id = "9507"
    stations['9507'].station_name = "Helenelunds Station"
    stations['9507'].distance = 16
    stations['9507'].lines = {36: 2}
    stations['9507'].traffic_type = "Trains"

    stations['3748'].station_id = "3748"
    stations['3748'].station_name = "Kista Alléväg"
    stations['3748'].distance = 5
    stations['3748'].lines = {514: 1, 627: 2}
    stations['3748'].traffic_type = "Buses"

    print_header()

    # Loop through all stations and:
    # (1) fetch data from API
    # (2) print relevant departures
    for s, o in stations.iteritems():
        o.api_data = get_api_json_data(API_KEY, o.station_id)
        o.print_departures()

if __name__ == '__main__':
    main()
