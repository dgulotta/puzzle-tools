"""
Utilities for scraping data for html and csv files.  See the
enumerations_web module for example uses.
"""

from bs4 import BeautifulSoup
from puzzletools.enumeration import EnumerationMeta
import csv, io

class Raw:
    """
    A tag indicating that raw HTML is being requested.

        >>> t=HTMLTable.from_data('''<html><table class="wikitable">
        ...    <tr><td>text</td></tr></table></html>''')
        >>> next(t.rows())[0]
        'text'
        >>> next(t.rows())[Raw(0)]
        <td>text</td>
    """

    def __init__(self,data):
        self.data=data

class Row:
    def __init__(self,nodes):
        self.nodes = nodes
        self.text = [node.text.strip() for node in nodes]

    def __getitem__(self,idx):
        if isinstance(idx, Raw):
            return self.nodes[idx.data]
        else:
            return self.text[idx]

    def __iter__(self):
        return iter(self.text)

    def __len__(self):
        return len(self.text)

class HTMLTable:
    def __init__(self,node):
        self.node = node

    def rows(self):
        for row in self.node.find_all('tr'):
            if not row.find('td'):
                continue
            cells = []
            for cell in row.find_all(['td','th']):
                colspan=int(cell.attrs.get('colspan',1))
                for _ in range(colspan):
                    cells.append(cell)
            yield Row(cells)

    @staticmethod
    def from_data(data,tablenum=0):
        if isinstance(data,bytes):
            data = data.decode()
        if not isinstance(data,BeautifulSoup):
            data = BeautifulSoup(data,'lxml')
        for t in data.find_all(attrs={'style':'display:none;speak:none'}):
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
        data = io.StringIO(data.decode(enc))
    elif isinstance(data,str):
        data = io.StringIO(data)
    elif isinstance(data,io.BufferedIOBase):
        data = io.TextIOWrapper(data,encoding=enc)
    reader=csv.reader(data)
    if headers:
        next(reader)
    yield from reader

def _fieldfunc(n,f):
    if isinstance(f,str):
        return lambda r: r[n]
    trans = lambda f: f
    idx = n
    for e in f[1:]:
        if callable(e):
            trans = e
        else:
            idx = e
    return lambda r: trans(r[idx])

def _fieldname(f):
    if isinstance(f,str):
        return f
    else:
        return f[0]

def make_enumeration(name,fields,data,display_key=None):
    fieldfuncs = [_fieldfunc(n,f) for n,f in enumerate(fields)]
    classdict={
        'fields': [_fieldname(f) for f in fields],
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
