#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc": {"pm1": 5.1, "pm2p5": 22.7, "pm10": 195.1, ' \
       '"per": 5.0, "bin1": [77, 38, 52, 39, 9, 15, 9, 2], "bin2": [4, 1, 2, 4, 0, 0, 0, 0], ' \
       '"mtf1": 30, "mtf3": 34, "mtf5": 34, "mtf7": 39}}}'
print(jstr)
print("-")


# --------------------------------------------------------------------------------------------------------------------

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)
print("-")

datum = PathDict(jdict)
print(datum)
print("-")

path1 = "val.opc.bin1"
print("path:%s" % path1)

has_path = datum.has_path(path1)
print("has_path:%s" % has_path)
print("-")

path2 = "val.opc.bin1.0"
print("path:%s" % path2)

has_path = datum.has_path(path2)
print("has_path:%s" % has_path)
print("-")

nodes = datum.node(path1)
print("nodes:%s" % str(nodes))
print("=")

path = "val.opx.bin1.0"
print("path:%s" % path)

has_path = datum.has_path(path)
print("has_path:%s" % has_path)

try:
    node = datum.node(path)
    print("node:%s" % node)
except Exception as ex:
    print(type(ex).__name__)
print("=")


# --------------------------------------------------------------------------------------------------------------------

target = PathDict()
print(target)
print("-")

print(datum)
print("-")

target.copy(datum, "rec")
print(target)
print("-")

path1 = "val.opc.bin1.0"
print(path1)
print("-")

path2 = "val.opc.bin2"
print(path2)
print("-")

path3 = "val.opc.bin1.1"
print(path3)
print("-")

target.copy(datum, path1)
print(target)
print("-")

source = "val.opc.extra"
print(source)
print("-")

target.append("val.opc.extra", "hello")
print(target)
print("-")

target.append("val.opc" + ".number", 123.34)
print(target)
print("-")

jstr = JSONify.dumps(target.node())
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)
print("-")

target = PathDict(jdict)
print(target)
print("-")
