#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lägg till modulen för pendeltåg
import trains
# Lägg till modulen för bussar
import buses

# trains.setStationId("9507")
# trains.setWalkTime(16)
# trains.setTimeWindow("60")

# API-nyckel: 72e87e92af514d73830ba8cf89b8197d
key = "72e87e92af514d73830ba8cf89b8197d"

# Exekvera pendeltågssökning
trains.getTrains(key, "9507", "60", 16)

# Exekvera buss-sökning
buses.getBuses(key, "3747", "30", 5)
