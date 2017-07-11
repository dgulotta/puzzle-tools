"""
Subway station data.  This module downloads data from Transitland, whereas
the subway functions in the enumerations_web module download data from
Wikipedia.
"""

import json
from urllib.request import urlopen
from puzzletools.table_parser import make_enumeration

_api_url='https://transit.land/api/v1/'

def _make_request(query,args):
    args.append(('per_page',1000))
    argstr='&'.join('{}={}'.format(*arg) for arg in args)
    url='{}{}?{}'.format(_api_url,query,argstr)
    return json.loads(urlopen(url).read().decode())[query]

class _Adder:
    def __init__(self):
        self.seen = {}
        self.data = []

    # New York has duplicate station names, but the line data are wrong
    # so deduping them isn't a big deal
    def __call__(self,st,lines):
        item = self.seen.get(st)
        if item is None:
            self.seen[st]=lines
            self.data.append((st,lines))
        else:
            for l in lines:
                if l not in item:
                    item.append(l)

class Subway:
    """
    A subway system.  The class's methods download data about the system
    from Transitland.  To add a new subway system, you just need to
    subclass this class and set the `operator` variable.  To determine the
    appropriate value of this variable, go to
    https://transit.land/feed-registry.
    """

    types = 'metro'

    @classmethod
    def stations(cls):
        """
        Returns an enumeration of this system's stations.
        """
        return make_enumeration(cls._enum_name(),
            [('name',0),('lines',1)],cls._rows(),'name')

    @classmethod
    def _rows(cls):
        raw=cls.stations_raw()
        adder=_Adder()
        for rec in raw:
            lines=[r['route_name'] for r in rec['routes_serving_stop']]
            adder(cls._parse_name(rec['name']),lines)
        return adder.data

    @classmethod
    def stations_raw(cls):
        """
        Returns data about this system's stations in JSON format.
        """
        args=[('served_by',cls.operator),('served_by_vehicle_types',cls.types)]
        return _make_request('stops',args)

    @classmethod
    def _enum_name(cls):
        return cls.__name__+'Station'

    @classmethod
    def _parse_name(cls,name):
        return name

class MBTA(Subway):
    operator = 'o-drt-mbta'
    types = 'metro,tram'

    @classmethod
    def _parse_name(cls,s):
        return s.split(' -')[0]

class NewYork(Subway):
    operator='o-dr5r-nyct'

class BART(Subway):
    operator='o-9q9-bart'

class Washington(Subway):
    operator='o-dqc-met'

    @classmethod
    def _parse_name(cls,name):
        idx=name.rfind(' METRO')
        if idx>0:
            name=name[:idx]
        return name.title()

class Paris(Subway):
    operator='o-u09t-metro'

class London(Subway):
    operator='o-gcpv-transportforlondon'

    @classmethod
    def _parse_name(cls,name):
        return name.replace(' Underground Station','')
