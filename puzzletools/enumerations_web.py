from puzzletools.enumeration import EnumerationMeta
from puzzletools.enumerations import State
from puzzletools.table_parser import csv_rows, HTMLTable, allow_none, Raw, view
from puzzletools.morse import dash_to_hyphen
from urllib.request import urlopen
from time import sleep
import datetime
import unicodedata, string, re
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import itertools
import cattr
from typing import Optional, Sequence

def download_wikitable(url,tablenum=0):
    return HTMLTable.from_data(urlopen(url).read(),tablenum).rows()

def download_csv(url,headers=False,enc='utf-8'):
    return csv_rows(urlopen(url).read(),headers,enc)

def strpdate(s,fmt):
    return datetime.datetime.strptime(s,fmt).date()

def _id_hook(data, cl):
    return data

_conv = cattr.Converter()
_conv.register_structure_hook(datetime.date, _id_hook)

def load_enumeration(cls, fields, rows):
    return [_conv.structure_attrs_fromtuple(row, cls) for row in view(rows, fields)]

class Country(metaclass=EnumerationMeta):
    name: str
    alpha2: str
    alpha3: str
    numeric: int
    independent: bool

def _countries():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/ISO_3166-1',1)
    fields = [ 0, 1, 2, 3, (5, lambda x: x=='Yes')]
    return load_enumeration(Country, fields, rows)

Country.set_items_lazy(_countries)

def _us_states():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')
    fields = [ 0, 1, 2, (4, lambda x: strpdate(x.replace('.',''),'%b %d, %Y')) ]
    return load_enumeration(State,fields,rows)

class ResistorColor(metaclass=EnumerationMeta):
    name: str
    code: str
    ral: Optional[int]
    sigfig: Optional[int]
    log_multiplier: int
    tolerance: str
    tolerance_letter: Optional[str]
    temp_coeff: Optional[int]
    temp_coeff_letter: Optional[str]

def _resistor_colors():
    rows_ext = download_wikitable('https://en.m.wikipedia.org/wiki/Electronic_color_code')
    rows = itertools.islice(rows_ext,1,None)
    lett=lambda x : x if x.isalpha() else None
    fields = [
        0,
        1,
        (2, allow_none(int)),
        (3, allow_none(int)),
        (4, lambda x: int(dash_to_hyphen(x[3:]))),
        6,
        (7, lett),
        (8, allow_none(int)),
        (9, lett)]
    return load_enumeration(ResistorColor, fields, rows)

ResistorColor.set_items_lazy(_resistor_colors)

class Zodiac(metaclass=EnumerationMeta):
    name: str
    symbol: str
    start: datetime.date
    end: datetime.date

def _zodiac():
    def parse_date(n):
        def pd(d):
            s=d.split('\u2013')
            if len(s)==2:
                return strpdate(s[n].strip(),'%d %B')
            else:
                return None
        return pd
    def lookup(s):
        if s=='Scorpio':
            s='Scorpius'
        return unicodedata.lookup(s)
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/Zodiac',1)
    fields = [ 0, (0, lookup), (2, parse_date(0)), (2, parse_date(1)) ]
    return load_enumeration(Zodiac,fields,rows)

Zodiac.set_items_lazy(_zodiac)

class Currency(metaclass=EnumerationMeta):
    code: str
    number: int
    name: str
    countries: Sequence[str]

def _currency():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/ISO_4217', 1)
    fields = [ 0, 1, 3, (Raw(4), HTMLTable.wikilink_list_format) ]
    return load_enumeration(Currency,fields,rows)

Currency.set_items_lazy(_currency)

class Language(metaclass=EnumerationMeta):
    name: str
    native_name: str
    code: str

def _language():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/List_of_ISO_639-1_codes')
    fields = [2, 3, 4]
    return load_enumeration(Language,fields,rows)

Language.set_items_lazy(_language)

_course_url_re = re.compile('m([0-9A-Z]+)a.html')
_newline_strip_re = re.compile('\n.*')

def mit_subject_listing():
    entries=[]
    soup = BeautifulSoup(urlopen('http://student.mit.edu/catalog/index.cgi'),'lxml')
    for elt in soup.find_all('a'):
        m = _course_url_re.match(elt.attrs['href'])
        entries.extend(mit_subject_listing_by_course(m.groups()[0]))
    return entries

def mit_subject_listing_by_course(num):
    num=str(num)
    entries=[]
    for l in string.ascii_lowercase:
        try:
            soup=BeautifulSoup(urlopen('http://student.mit.edu/catalog/m%s%s.html'%(num,l)),'lxml')
            entries.extend(_newline_strip_re.sub('',elt.text).split(' ',1) for elt in soup.find_all('h3'))
            sleep(1)
        except HTTPError:
            break
    return entries

class LondonUnderground(metaclass=EnumerationMeta):
    name: str
    lines: Sequence[str]

def _london_underground_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_London_Underground_stations'
    rows = download_wikitable(url,0)
    fields = [0, (Raw(2), HTMLTable.wikilink_list_format)]
    return load_enumeration(LondonUnderground,fields,rows)

LondonUnderground.set_items_lazy(_london_underground_stations)

class MBTAStation(metaclass=EnumerationMeta):
    name: str
    lines: Sequence[str]

def _mbta_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_MBTA_subway_stations'
    rows = download_wikitable(url,1)
    fields = [0, (Raw(1),HTMLTable.wikilink_list_format)]
    return load_enumeration(MBTAStation,fields,rows)

MBTAStation.set_items_lazy(_mbta_stations)

_paris_sep_re = re.compile(r'\s*[&,]\s*')

class ParisMetro(metaclass=EnumerationMeta):
    name: str
    code: str
    lines: Sequence[str]

def _paris_metro_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_stations_of_the_Paris_M%C3%A9tro'
    rows = download_wikitable(url)
    fields = [0, 2, (3, lambda x: _paris_sep_re.split(x)) ]
    return load_enumeration(ParisMetro,fields,rows)

ParisMetro.set_items_lazy(_paris_metro_stations)

_washington_alt_re = re.compile(r'WMATA (\w+).svg')

def _washington_lines(node):
    lines = []
    for n in node.find_all('img'):
        m = _washington_alt_re.match(n.attrs.get('alt',''))
        if m:
            lines.append(m.groups()[0])
    return lines

class WashingtonMetro(metaclass=EnumerationMeta):
    name: str
    lines: Sequence[str]

def _washington_metro_stations():
    url='https://en.m.wikipedia.org/wiki/List_of_Washington_Metro_stations'
    rows = download_wikitable(url,2)
    fields = [0, (Raw(1),_washington_lines)]
    return load_enumeration(WashingtonMetro,fields,rows)

WashingtonMetro.set_items_lazy(_washington_metro_stations)

class Airport(metaclass=EnumerationMeta):
    name: str
    city: str
    country: str
    iata: str
    icao: str
    latitude: float
    longitude: float
    altitude: int
    utcoff: Optional[float]
    dst: str
    timezone: str

def _airports():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
    rows = download_csv(url,enc='iso-8859-1')
    fields = [ 1, 2, 3, 4, 5, 6, 7, 8, (9, allow_none(float)), 10, 11 ]
    return load_enumeration(Airport,fields,rows)

Airport.set_items_lazy(_airports)

class Airline(metaclass=EnumerationMeta):
    name: str
    alias: Optional[str]
    iata: str
    icao: str
    callsign: str
    country: str
    active: bool

def _airlines():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'
    rows = itertools.islice(download_csv(url,enc='iso-8859-1'),2,None)
    fields = [ 1, (2, lambda s: None if s==r'\N' else s), 3, 4, 5, 6,
        (7, lambda s: s=='Y') ]
    return load_enumeration(Airline,fields,rows)

Airline.set_items_lazy(_airlines)

class Stock(metaclass=EnumerationMeta):
    symbol: str
    name: str
    price: Optional[float]
    market_cap: Optional[float]
    ipo_yr: Optional[int]
    sector: str
    industry: str
    exchange: str

def _stock_table(name):
    urlbase='http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={}&render=download'
    table=download_csv(urlbase.format(name),headers=True)
    for r in table:
        r[9]=name
        yield r

def _stocks():
    rows = itertools.chain(*map(_stock_table,['NYSE','NASDAQ','AMEX']))
    fields = [ 0, 1, (2, allow_none(float)), (3, allow_none(float)),
        (5, allow_none(int)), 6, 7, 9 ]
    return load_enumeration(Stock,fields,rows)

Stock.set_items_lazy(_stocks)
