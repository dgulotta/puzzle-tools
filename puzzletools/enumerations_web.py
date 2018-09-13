from puzzletools.table_parser import (csv_rows, HTMLTable, allow_none,
    make_enumeration, Raw)
from puzzletools.morse import dash_to_hyphen
from urllib.request import urlopen
from time import sleep
import datetime
import unicodedata, string, re
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import itertools

def download_wikitable(url,tablenum=0):
    return HTMLTable.from_data(urlopen(url).read(),tablenum).rows()

def download_csv(url,headers=False,enc='utf-8'):
    return csv_rows(urlopen(url).read(),headers,enc)

def strpdate(s,fmt):
    return datetime.datetime.strptime(s,fmt).date()

def countries():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/ISO_3166-1',1)
    fields = [
        ('name',0),
        ('alpha2',1),
        ('alpha3',2),
        ('numeric',3,int),
        ('independent',5,lambda x: x=='Yes')]
    return make_enumeration('Country',fields,rows,'name')

# these are available offline now
def _us_states():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')
    fields = [
        ('name',0),
        ('abbr',1),
        ('capital',2),
        ('statehood',4,lambda x: strpdate(x.replace('.',''),'%b %d, %Y'))]
    return make_enumeration('State',fields,rows,'name')

def resistor_colors():
    rows_ext = download_wikitable('https://en.m.wikipedia.org/wiki/Electronic_color_code')
    rows = itertools.islice(rows_ext,1,None)
    lett=lambda x : x if x.isalpha() else None
    fields = [
        ('name',0),
        ('code',1),
        ('ral',2,allow_none(int)),
        ('sigfig',3,allow_none(int)),
        ('log_multiplier',4,lambda x: int(dash_to_hyphen(x[3:]))),
        ('tolerance',6),
        ('tolerance_letter',7,lett),
        ('temp_coeff',8,allow_none(int)),
        ('temp_coeff_letter',9,lett)]
    return make_enumeration('Color',fields,rows,'name')

def zodiac():
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
    fields = [
        ('name',0),
        ('symbol',0,lookup),
        ('start',2,parse_date(0)),
        ('end',2,parse_date(1))]
    return make_enumeration('Zodiac',fields,rows,'name')

def currency():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/ISO_4217')
    fields = [
        ('code',0),
        ('number',1,int),
        ('name',3),
        ('countries',Raw(4),HTMLTable.wikilink_list_format)]
    return make_enumeration('Currency',fields,rows,'name')

def languages():
    rows = download_wikitable('https://en.m.wikipedia.org/wiki/List_of_ISO_639-1_codes')
    fields = [('name',2), ('native_name',3), ('code',4)]
    return make_enumeration('Language',fields,rows,'name')

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

def london_underground_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_London_Underground_stations'
    rows = download_wikitable(url,0)
    fields = [('name',0),('lines',Raw(2),HTMLTable.wikilink_list_format)]
    return make_enumeration('LondonUnderground',fields,rows,'name')

def mbta_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_MBTA_subway_stations'
    rows = download_wikitable(url,1)
    fields = [('name',0), ('lines',Raw(1),HTMLTable.wikilink_list_format)]
    return make_enumeration('MBTAStations',fields,rows,'name')

_paris_sep_re = re.compile(r'\s*[&,]\s*')

def paris_metro_stations():
    url = 'https://en.m.wikipedia.org/wiki/List_of_stations_of_the_Paris_M%C3%A9tro'
    rows = download_wikitable(url)
    fields = [
        ('name',0),
        ('code',2),
        ('lines',3,lambda x: _paris_sep_re.split(x))]
    return make_enumeration('ParisMetro',fields,rows,'name')

def washington_metro_stations():
    url='https://en.m.wikipedia.org/wiki/List_of_Washington_Metro_stations'
    rows = download_wikitable(url,2)
    fields = [('name',0),('lines',Raw(1),HTMLTable.wikilink_list_format)]
    return make_enumeration('WashingtonMetro',fields,rows,'name')

def airport_codes():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
    rows = download_csv(url,enc='iso-8859-1')
    fields = [
        ('name',1),
        ('city',2),
        ('country',3),
        ('iata',4),
        ('icao',5),
        ('latitude',6,float),
        ('longitude',7,float),
        ('altitude',8,int),
        ('utcoff',9,allow_none(float)),
        ('dst',10),
        ('timezone',11),
    ]
    return make_enumeration('Airport',fields,rows,'icao')

def airlines():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'
    rows = itertools.islice(download_csv(url,enc='iso-8859-1'),2,None)
    fields = [
        ('name',1),
        ('alias',2,lambda s: None if s==r'\N' else s),
        ('iata',3),
        ('icao',4),
        ('callsign',5),
        ('country',6),
        ('active',7,lambda s: s=='Y'),
    ]
    return make_enumeration('Airline',fields,rows,'callsign')

def _stock_table(name):
    urlbase='http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange={}&render=download'
    table=download_csv(urlbase.format(name),headers=True)
    for r in table:
        r[9]=name
        yield r

def stocks():
    rows = itertools.chain(*map(_stock_table,['NYSE','NASDAQ','AMEX']))
    fields = [
        ('symbol',0),
        ('name',1),
        ('price',2,allow_none(float)),
        ('market_cap',3,allow_none(float)),
        ('ipo_yr',5,allow_none(int)),
        ('sector',6),
        ('industry',7),
        ('exchange',9),
    ]
    return make_enumeration('Stock',fields,rows,'symbol')
