from collections import defaultdict
from unidecode import unidecode
import re

_sep_re = re.compile(r'[/_\-]+')
_alnumspace_re = re.compile(r'[^0-9A-Za-z ]')
_spaces_re = re.compile(r'\s+')

def normalize_alnum(s):
    s = unidecode(s).upper()
    s = s.replace('&',' AND ')
    s = _sep_re.sub(' ',s)
    s = _alnumspace_re.sub('',s)
    s = _spaces_re.sub(' ',s).strip()
    return s

class WordlistGenerator:
    def __init__(self):
        self.words = defaultdict(lambda : 0)

    def add(self,name,freq,func=lambda x,y: x+y):
        name = normalize_alnum(name)
        freq = int(freq)
        self.words[name]=func(self.words[name],freq)

    def write(self,filename,cutoff=0):
        l = [(v,k) for k,v in self.words.items() if v>=cutoff]
        l.sort(reverse=True)
        with open(filename,'w') as f:
            for v,k in l:
                print("%s\t%d"%(k,v),file=f)
