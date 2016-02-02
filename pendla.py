#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lägg till moduler för pendeltåg och bussar
import trains
import buses

# Importera lib för yaml-config
try:
    import yaml
except ImportError:
    print "Requires PyYAML module to function"
    exit()

try:
    with open("config.yml", 'r') as ymlfile:
        # läser config.yml och skapar en dict 'cfg' med alla värden
        cfg = yaml.load(ymlfile)
except IOError:
    print "No configuration file found!"
    print "Creating sample file 'config.yml'. Please edit and save this file before running the program again."
    # Skapar en dict med exempel-konfiguration, och skriver denna till en fil
    cfg = {}
    cfg['pendel'] = {'stationer': [{12345: {'tid': 15, 'linjer': [{123: {'riktning': 1}}, 456]}}]}
    cfg['buss'] = {'stationer': [{67890: {'tid': 5, 'linjer': [{12: {'riktning': 2}}]}}]}
    with file("config.yml", "w") as stream:
        yaml.dump(cfg, stream)

key = "72e87e92af514d73830ba8cf89b8197d"
timeWindow = "60"

# Iterera alla stationer i "pendel":
for station in cfg['pendel']['stationer']:
    trains.getTrains(key, station, timeWindow)





# Ändra dessa värden till de stations- och hållplatsID du vill se, samt önskat tidsfönster och tiden det tar dig att gå dit.
# (key, "<ID för hållplats/station>", "<tidsfönster>", <gångavstånd i minuter>)
# Exekvera pendeltågssökning
#trains.getTrains(key, "9507", "60", 16)
# Exekvera buss-sökning
#buses.getBuses(key, "3747", "30", 5)
