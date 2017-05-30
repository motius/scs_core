"""
Created on 29 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

report examples:
 8:27  up 6 mins, 2 users, load averages: 3.78 2.20 1.09
 9:31  up  1:09, 2 users, load averages: 0.82 0.96 1.00
07:02:40 up 2 days, 19:34,  0 users,  load average: 0.66, 0.65, 0.60

JSON example:
{"time": "2017-05-29T12:40:58.619+01:00", "up": {"days": 1, "hours": 19, "minutes": 34, "seconds": 0},
"users": 0, "load": {"av1": 0.66, "av5": 0.65, "av15": 0.6}}
"""

import re

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class UptimeDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_report(cls, time, report):
        # uptime...
        uptime = Timedelta.construct_from_uptime_report(report)

        # users...
        users_match = re.match('.*(\d+) user(?:s)?,', report)

        if users_match:
            fields = users_match.groups()
            users = int(fields[0])

        else:
            users = None

        # load...
        load = UptimeLoad.construct_from_uptime_report(report)

        return UptimeDatum(time, uptime, users, load)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        time = LocalizedDatetime.construct_from_iso8601(jdict.get('time'))
        uptime = Timedelta.construct_from_jdict(jdict.get('up'))
        users = int(jdict.get('users'))
        load = UptimeLoad.construct_from_jdict(jdict.get('load'))

        return UptimeDatum(time, uptime, users, load)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, time, uptime, users, load):
        """
        Constructor
        """
        self.__time = time                  # LocalizedDatetime
        self.__uptime = uptime              # Timedelta
        self.__users = users                # int
        self.__load = load                  # UptimeLoad


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['time'] = self.time
        jdict['up'] = self.uptime
        jdict['users'] = self.users
        jdict['load'] = self.load

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def time(self):
        return self.__time


    @property
    def uptime(self):
        return self.__uptime


    @property
    def users(self):
        return self.__users


    @property
    def load(self):
        return self.__load


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UptimeDatum:{time:%s, uptime:%s, users:%s, load:%s}" %  (self.time, self.uptime, self.users, self.load)


# --------------------------------------------------------------------------------------------------------------------

class UptimeLoad(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_uptime_report(cls, report):
        load_match = re.match('.*load average(?:s)?: (\d+\.\d+)(?:,)? (\d+\.\d+)(?:,)? (\d+\.\d+)', report)

        if load_match:
            fields = load_match.groups()
            return UptimeLoad(fields[0], fields[1], fields[2])

        else:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        av1 = jdict.get('av1')
        av5 = jdict.get('av5')
        av15 = jdict.get('av15')

        return UptimeLoad(av1, av5, av15)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, av1, av5, av15):
        """
        Constructor
        """
        self.__av1 = Datum.float(av1, 2)                  # one-minute load average
        self.__av5 = Datum.float(av5, 2)                  # five-minute load average
        self.__av15 = Datum.float(av15, 2)                # 15-minute load average


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['av1'] = self.av1
        jdict['av5'] = self.av5
        jdict['av15'] = self.av15

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def av1(self):
        return self.__av1


    @property
    def av5(self):
        return self.__av5


    @property
    def av15(self):
        return self.__av15


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UptimeLoad:{av1:%s, av5:%s, av15:%s}" % (self.av1, self.av5, self.av15)