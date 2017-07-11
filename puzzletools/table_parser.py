from bs4 import BeautifulSoup
from puzzletools.enumeration import EnumerationMeta
from io import StringIO
import csv

class HTMLTable:
    def __init__(self,node):
        self.node = node

    def rows(self,fmt={}):
        for row in self.rows_dom():
            yield [fmt.get(n,self.parse_node)(c) for n,c in enumerate(row)]

    def rows_dom(self):
        for row in self.node.find_all('tr'):
            if not row.find('td'):
                continue
            cells = []
            for cell in row.find_all(['td','th']):
                colspan=int(cell.attrs.get('colspan',1))
                for _ in range(colspan):
                    cells.append(cell)
            yield cells

    @staticmethod
    def parse_node(node):
        return node.text.strip()

    @staticmethod
    def from_data(data,tablenum=0):
        if isinstance(data,bytes):
            data = data.decode()
        if not isinstance(data,BeautifulSoup):
            data = BeautifulSoup(data,'lxml')
        for t in data.find_all(attrs={'style':'display:none;'}):
            t.decompose()
        for t in data.find_all('sup',attrs={'class':'reference'}):
            t.decompose()
        node=data.find_all('table',class_='wikitable')[tablenum]
        return HTMLTable(node)

    @staticmethod
    def wikilink_list_format(cell):
        l = []
        for t in cell.find_all('a'):
            text=t.text.strip()
            if text:
                l.append(text)
        return l

def csv_rows(data,headers=False,enc='utf-8'):
    if isinstance(data,bytes):
        data = StringIO(data.decode(enc))
    elif isinstance(data,str):
        data = StringIO(data)
    reader=csv.reader(data)
    if headers:
        next(reader)
    yield from reader

def _fieldfunc(idx,fmt=None):
    if callable(idx):
        return idx
    elif fmt:
        return lambda r: fmt(r[idx])
    else:
        return lambda r: r[idx]

def make_enumeration(name,fields,data,display_key=None):
    fieldfuncs = [_fieldfunc(*f[1:]) for f in fields]
    classdict={
        'fields': [f[0] for f in fields],
        'data': [[f(r) for f in fieldfuncs] for r in data]
    }
    if display_key:
        classdict['display_key']=display_key
    return EnumerationMeta(name,(),classdict)

def allow_none(f):
    def apply(n):
        try:
            return f(n)
        except ValueError:
            return None
    return apply
