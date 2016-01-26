#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
from datetime import datetime, date
from time import mktime, time

# Lägg till linux terminal färg-kommandon
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#api.sl.se/api2/realtimedepartures.<FORMAT>?key=<DIN API NYCKEL>&siteid=<SITEID>&timewindow=<TIMEWINDOW>

### Konfiguration ###

# API-nyckel: 72e87e92af514d73830ba8cf89b8197d
key = "72e87e92af514d73830ba8cf89b8197d"
# ID för stationen du vill åka ifrån
station = "3747"
# Tidsfönster i minuter
tw = "30"
# Önskade linjer
lines = ("627", "514")
# Tid i minuter att gå till stationen
walk = 5

###

url = "http://api.sl.se/api2/realtimedepartures.json?key="+key+"&siteid="+station+"&timewindow="+tw
#raw json data into 'instanse'
jsonData = urlopen(url)
#parsed json data into 'dict'
jsonParsed = json.load(jsonData)

# Vi vill bara se pendeltåg
trains = jsonParsed['ResponseData']['Buses']
# gör om till sekunder
walk = walk*60

# output enligt nedan
# "X min (tid/realtid) Destination - Meddelande"

# Printa ut lite kolumner
print color.GREEN+color.BOLD+'%-8s' % "Avgång",
print '%-11s' % "Tid",
print "Linje",
print "Destination"
print

for i in trains:
    # Vi åker bara norrut (2)
    if i['LineNumber'] in lines:

        currEpochTime = int(time())
        timeTableEpoch = int(mktime(datetime.strptime(i['TimeTabledDateTime'], "%Y-%m-%dT%H:%M:%S").timetuple()))
        expectedEpoch = int(mktime(datetime.strptime(i['ExpectedDateTime'], "%Y-%m-%dT%H:%M:%S").timetuple()))
        timeTablePretty = datetime.strftime(datetime.strptime(i['TimeTabledDateTime'], "%Y-%m-%dT%H:%M:%S"), "%H:%M")
        ExpectedPretty = datetime.strftime(datetime.strptime(i['ExpectedDateTime'], "%Y-%m-%dT%H:%M:%S"), "%H:%M")

        # Om tiden till tåget går är mindre än tiden det tar att gå
        if (timeTableEpoch-currEpochTime) < walk:
            continue

        # Visa "DisplayTime"
        print color.BOLD + color.YELLOW + '%-7s' % i['DisplayTime'].encode('utf-8') + color.END,

        # Om realtid matchar tidtabellen
        if timeTableEpoch == expectedEpoch:
            # Visa tabelltid
            print '%-11s' % timeTablePretty,
        # ...Annars printa både tabelltid samt ny tid
        else:
            # Visa tabelltid
            print '%-11s' % (timeTablePretty+"/"+color.RED+ExpectedPretty+color.END),

        # Visa destination
        print color.DARKCYAN+'%-5s' % i['LineNumber'],
        print color.YELLOW+'%-11s' % i['Destination'].encode('utf-8')+color.END

        # Om det finns avvikelser, printa meddelandet
        if i['Deviations']:
            print color.DARKCYAN+"- " + i['Deviations'][0]['Text'][:80]+color.END
