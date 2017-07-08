from puzzletools.table_parser import parse_wikitable, Table, allow_none
from puzzletools.morse import dash_to_hyphen
from urllib.request import urlopen
from time import strptime, sleep
import unicodedata, string, re
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from io import StringIO

def download_wikitable(url,tablenum=0,fmt=None):
    return parse_wikitable(urlopen(url),tablenum,fmt)

def download_csv(url,fmt=None,enc='utf-8'):
    return Table.from_csv(StringIO(urlopen(url).read().decode(enc)),fmt)

def countries():
    return download_wikitable('https://en.m.wikipedia.org/wiki/ISO_3166-1',1).make_enumeration('Country',[('name',0),('alpha2',1),('alpha3',2),('numeric',3,int),('independent',5,lambda x: x=='Yes')],'name')

def us_states():
    return download_wikitable('https://en.m.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States').make_enumeration('State',[('name',0),('abbr',1),('capital',2),('statehood',4,lambda x: strptime(x,'%B %d, %Y'))],'name')

def resistor_colors():
    t=download_wikitable('https://en.m.wikipedia.org/wiki/Electronic_color_code')
    t.data=t.data[:12]
    lett=lambda x : x if x.isalpha() else None
    return t.make_enumeration('Color',[('name',0),('log_multiplier',2,lambda x: int(dash_to_hyphen(x[3:]))),('tolerance',3),('tolerance_letter',4,lett),('temp_coeff',5,lambda x: int(x) if x.isnumeric() else None),('temp_coeff_leter',6,lett)],'name')

def zodiac():
    def parse_date(n):
        def pd(d):
            if d=='n/a':
                return None
            else:
                return strptime(d.split('\u2013')[n].strip(),'%d %B')
        return pd
    def lookup(s):
        if s=='Scorpio':
            s='Scorpius'
        return unicodedata.lookup(s)
    return download_wikitable('https://en.m.wikipedia.org/wiki/Zodiac',1).make_enumeration('Zodiac',[('name',0),('symbol',0,lookup),('start',2,parse_date(0)),('end',2,parse_date(1))],'name')

def currency():
    return download_wikitable('https://en.m.wikipedia.org/wiki/ISO_4217').make_enumeration('Currency',[('code',0),('number',1,lambda x : int(x) if x.isnumeric() else None),('name',3),('countries',4,lambda x: [y.strip() for y in x.split(',')])],'name')

def languages():
    return download_wikitable('https://en.m.wikipedia.org/wiki/List_of_ISO_639-1_codes').make_enumeration('Language',[('name',2),('native_name',3),('code',4)],'name')

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
    fmt={ 2 : Table.wikilink_list_format }
    url='https://en.m.wikipedia.org/wiki/List_of_London_Underground_stations'
    return download_wikitable(url,0,fmt).make_enumeration('LondonUnderground',[('name',0),('lines',2)],'name')

def mbta_stations():
    fmt={ 1 : Table.wikilink_list_format }
    url='https://en.m.wikipedia.org/wiki/List_of_MBTA_subway_stations'
    return download_wikitable(url,1,fmt).make_enumeration('MBTAStations',[('name',0),('lines',1)],'name')

_paris_sep_re = re.compile(r'\s*[&,]\s*')

def paris_metro_stations():
    url='https://en.m.wikipedia.org/wiki/List_of_stations_of_the_Paris_M%C3%A9tro'
    return download_wikitable(url).make_enumeration('ParisMetro',[('name',0),('code',2),('lines',3,lambda x: _paris_sep_re.split(x))],'name')

def washington_metro_stations():
    url='https://en.m.wikipedia.org/wiki/List_of_Washington_Metro_stations'
    fmt={ 1 : Table.wikilink_list_format }
    return download_wikitable(url,2,fmt).make_enumeration('WashingtonMetro',[('name',0),('lines',1)],'name')

def airport_codes():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
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
    return download_csv(url,enc='iso-8859-1').make_enumeration('Airport',fields,'icao')

def airlines():
    url='https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'
    fields = [
        ('name',1),
        ('alias',2,lambda s: None if s==r'\N' else s),
        ('iata',3),
        ('icao',4),
        ('callsign',5),
        ('country',6),
        ('active',7,lambda s: s=='Y'),
    ]
    return download_csv(url,enc='iso-8859-1').make_enumeration('Airline',fields,'callsign')
