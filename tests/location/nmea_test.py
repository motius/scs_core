#!/usr/bin/env python3

"""
Created on 31 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.location.gpgga import GPGGA
from scs_core.location.gpgll import GPGLL
from scs_core.location.gpgsa import GPGSA
from scs_core.location.gpgsv import GPGSV
from scs_core.location.gprmc import GPRMC
from scs_core.location.gpvtg import GPVTG
from scs_core.location.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

line = "$GPGGA,103228.00,5049.37823,N,00007.37872,W,2,07,1.85,34.0,M,45.4,M,,0000*75"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGGA.construct(s)
print(message)
print("-")

lat = message.loc.deg_lat()
lng = message.loc.deg_lng()
print("%f, %f" % (lat, lng))
print("-")

print(message.time.as_iso8601())
print("=")


# --------------------------------------------------------------------------------------------------------------------

line = "$GPGLL,5049.37823,N,00007.37872,W,103228.00,A,D*7F"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGLL.construct(s)
print(message)
print("-")

lat = message.loc.deg_lat()
lng = message.loc.deg_lng()
print("%f, %f" % (lat, lng))
print("-")

print(message.time.as_iso8601())
print("=")


# --------------------------------------------------------------------------------------------------------------------

line = "$GPGSV,3,1,10,23,38,230,44,29,71,156,47,07,29,116,41,08,09,081,36*7F"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGSV.construct(s)
print(message)
print("-")


line = "$GPGSV,3,2,10,10,07,189,,05,05,220,,09,34,274,42,18,25,309,44*72"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGSV.construct(s)
print(message)
print("-")


line = "$GPGSV,3,3,10,26,82,187,47,28,43,056,46*77"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGSV.construct(s)
print(message)
print("=")


# --------------------------------------------------------------------------------------------------------------------

line = "$GPGSA,A,3,23,29,07,08,09,18,26,28,,,,,1.94,1.18,1.54*0D"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPGSA.construct(s)
print(message)
print("=")


# --------------------------------------------------------------------------------------------------------------------

line = "$GPRMC,083559.00,A,4717.11437,N,00833.91522,E,0.004,77.52,091202,,,A*57"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPRMC.construct(s)
print(message)
print("-")

lat = message.loc.deg_lat()
lng = message.loc.deg_lng()
print("%f, %f" % (lat, lng))
print("-")

print(message.datetime.as_iso8601())
print("=")


# --------------------------------------------------------------------------------------------------------------------

line = "$GPVTG,77.52,T,,M,0.004,N,0.008,K,A*06"
print(line)

s = NMEASentence.construct(line)
print(s)

message = GPVTG.construct(s)
print(message)
print("=")
