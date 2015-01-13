from unidecode import unidecode
import re

sep_re = re.compile(r'[/_\-]+')
alnumspace_re = re.compile(r'[^0-9A-Za-z ]')
spaces_re = re.compile(r'\s+')

def normalize_alnum(s):
    s = unidecode(s).upper()
    s = s.replace('&',' AND ')
    s = sep_re.sub(' ',s)
    s = alnumspace_re.sub('',s)
    s = spaces_re.sub(' ',s).strip()
    return s
