from puzzletools.table_parser import parse_wikitable
from puzzletools.morse import dash_to_hyphen
from urllib.request import urlopen
from time import strptime
import unicodedata

def download_wikitable(url,tablenum=0):
    return parse_wikitable(urlopen(url),tablenum)

def countries():
    return download_wikitable('https://en.m.wikipedia.org/wiki/ISO_3166-1').make_enumeration('Country',[('name',0),('alpha2',1),('alpha3',2)],'name')

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
