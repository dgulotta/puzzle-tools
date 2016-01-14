from puzzletools.table_parser import parse_wikitable
from urllib.request import urlopen
from time import strptime

def download_wikitable(url,tablenum=0):
    return parse_wikitable(urlopen(url),tablenum)

def countries():
    return download_wikitable('https://en.m.wikipedia.org/wiki/ISO_3166-1').make_enumeration('Country',[('name',0),('alpha2',1),('alpha3',2)],'name')

def us_states():
    return download_wikitable('https://en.m.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States').make_enumeration('State',[('name',0),('abbr',1),('capital',2),('statehood',4,lambda x: strptime(x,'%B %d, %Y'))],'name')
