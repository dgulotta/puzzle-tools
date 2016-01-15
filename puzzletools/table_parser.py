from bs4 import BeautifulSoup
from puzzletools.enumeration import EnumerationMeta

class Table:

    def __init__(self):
        self.headers=[]
        self.data=[]

    def make_enumeration(self,name,fields,display_key=None):
        fieldfuncs=[self._fieldfunc(*f[1:]) for f in fields]
        classdict={
            'fields' : [f[0] for f in fields],
            'data' : [[f(r) for f in fieldfuncs] for r in self.data]
        }
        if display_key:
            classdict['display_key']=display_key
        return EnumerationMeta(name,(),classdict)

    @staticmethod
    def _fieldfunc(idx,fmt=lambda x: x):
        if callable(idx):
            return idx
        else:
            return lambda r,i=idx,f=fmt: f(r[i])

    def _getdata(row,index):
        try:
            return row[index]
        except IndexError:
            pass
        try:
            return next(index)
        except TypeError:
            pass
        raise TypeError('Expected index to be an integer or iterator')

    @staticmethod
    def from_soup(soup):
        table=Table()
        all_rows=soup.find_all('tr')
        if not all_rows:
            return table
        for elt in all_rows[0].find_all('th'):
            colspan=int(elt.attrs.get('colspan',1))
            for n in range(colspan):
                table.headers.append(elt.text)
        for row in all_rows:
            if not row.find('td'):
                continue
            cells=row.find_all(['td','th'])
            if cells:
                rowdata=[]
                table.data.append(rowdata)
                for cell in cells:
                    colspan=int(cell.attrs.get('colspan',1))
                    for n in range(colspan):
                        rowdata.append(cell.text.strip())
        return table

def parse_wikitable(data,tablenum=0):
    soup=BeautifulSoup(data)
    for t in soup.find_all(attrs={'style':'display:none;'}):
        t.decompose()
    for t in soup.find_all('sup',attrs={'class':'reference'}):
        t.decompose()
    elt=soup.find_all('table',class_='wikitable')[tablenum]
    return Table.from_soup(elt)
