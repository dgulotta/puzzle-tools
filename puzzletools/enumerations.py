from puzzletools.enumeration import EnumerationMeta
from puzzletools.datafiles import load_tsv
import datetime

class ChemicalElement(metaclass=EnumerationMeta):
    number: int
    symbol: str
    name: str

ChemicalElement.items = load_tsv('elements.tsv', ChemicalElement)

class State(metaclass=EnumerationMeta):
    name: str
    abbr: str
    capital: str
    statehood: datetime.date

State.items = load_tsv('states.tsv', State)

_short_symbols = { e.symbol for e in ChemicalElement.items if len(e.symbol)<=2 }

def parse_as_element_symbols(s):
    '''
    Given a string `s`, returns a tuple whose first element is the number of
    ways of parsing `s` as a sequence of element symbols, and whose second
    element is one such parsing (or `None` if none exists).

        >>> parse_as_element_symbols('the south')
        (1, ['Th', 'Es', 'O', 'U', 'Th'])
    '''
    s = ''.join(c for c in s if c.isalpha())
    partial = [[] if i==0 else None for i in range(len(s)+1)]
    count = [1 if i==0 else 0 for i in range(len(s)+1)]
    for i in range(len(s)):
        if count[i]:
            for j in range(1,3):
                if i+j<=len(s):
                    sym = s[i:i+j].title()
                    if sym in _short_symbols:
                        count[i+j]+=count[i]
                        if partial[i+j] is None:
                            partial[i+j]=partial[i]+[sym]
    return (count[-1],partial[-1])
