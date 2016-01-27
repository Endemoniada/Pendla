#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lägg till moduler för pendeltåg och bussar
import trains
import buses

key = "72e87e92af514d73830ba8cf89b8197d"

# Ändra dessa värden till de stations- och hållplatsID du vill se, samt önskat tidsfönster och tiden det tar dig att gå dit.
# (key, "<ID för hållplats/station>", "<tidsfönster>", <gångavstånd i minuter>)
# Exekvera pendeltågssökning
trains.getTrains(key, "9507", "60", 16)
# Exekvera buss-sökning
buses.getBuses(key, "3747", "30", 5)
