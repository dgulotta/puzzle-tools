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
        validate=cls._station_validator()
        for rec in raw:
            lines=[r['route_name'] for r in rec['routes_serving_stop']]
            row=validate([rec['name'],lines])
            if row is not None:
                yield row

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
    def _station_validator(cls):
        def validate(s):
            s[0]=cls._parse_name(s[0])
            return s
        return validate

    @classmethod
    def _parse_name(cls,name):
        return name


class MBTA(Subway):
    operator = 'o-drt-mbta'
    types = 'metro,tram'

    @classmethod
    def _station_validator(cls):
        seen={}
        def validate(s):
            name=s[0].split(' -')[0]
            item = seen.get(name)
            if item is None:
                s[0]=name
                seen[name]=s[1]
                return s
            else:
                for l in s[1]:
                    if l not in item:
                        item.append(l)
        return validate

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
