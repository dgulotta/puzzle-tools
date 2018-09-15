"""
Encoder and decoder for flag semaphore.
    >>> from puzzletools.code import StringEncoder, StringDecoder
    >>> enc = StringEncoder(encoder=StatefulSemaphoreEncoder(DirectionRogue))
    >>> enc('hello')
    'HB JU UB UB HY'
    >>> dec = StringDecoder(decoder=StatefulSemaphoreDecoder(DirectionNumpad))
    >>> dec('62 19 21 23 / 34 29 61 21 48 41 47 64 29')
    'FLAG SEMAPHORE'
"""

from puzzletools.code import Code, reverse_dict
from puzzletools.datafiles import load_tsv

class Direction(Code):

    @classmethod
    def to_parent(cls,d):
        return cls.parent.dirs[cls.dirs.index(d)]

    @classmethod
    def from_parent(cls,d):
        return cls.dirs[cls.parent.dirs.index(d)]

class DirectionUnicode(Direction):
    dirs = list('\u2192\u2197\u2191\u2196\u2190\u2199\u2193\u2198')
    list_constructor = ''.join

Direction.parent=DirectionUnicode

class DirectionPhonepad(Direction):
    dirs = list('63214789')
    list_constructor = ''.join

class DirectionNumpad(Direction):
    dirs = list('69874123')
    list_constructor = ''.join

class DirectionRogue(Direction):
    dirs = list('LUKYHBJN')
    list_constructor = ''.join

class DirectionCompass(Direction):
    dirs = 'E NE N NW W SW S SE'.split(' ')

class DirectionCartesian(Direction):
    dirs = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

class StatefulSemaphoreEncoder:

    alpha_to_semaphore = dict(load_tsv('semaphore.tsv'))

    def __init__(self,dirs=DirectionUnicode):
        self.mapping = { k : ''.join(map(dirs.from_parent,v)) for k,v in self.alpha_to_semaphore.items() }
        self.reset()

    def reset(self):
        self.numeric=False

    def __call__(self,chars):
        l = []
        for s in chars:
            if s.isnumeric():
                if not self.numeric:
                    l.append(self.mapping['#'])
                    self.numeric=True
                if s=='0':
                    l.append(self.mapping['K'])
                else:
                    l.append(self.mapping[chr(ord(s)+16)])
            else:
                if self.numeric:
                    l.append(self.mapping['J'])
                    self.numeric=False
                l.append(self.mapping[s])
        return l

class StatefulSemaphoreDecoder:

    semaphore_to_alpha = { frozenset(b): a for a, b
        in StatefulSemaphoreEncoder.alpha_to_semaphore.items() }

    def __init__(self,dirs=DirectionPhonepad):
        self.mapping = { frozenset(dirs.from_parent(c) for c in k) : v for k,v in self.semaphore_to_alpha.items() }
        self.reset()

    def reset(self):
        self.numeric=False

    def __call__(self,data):
        l = []
        for s in data:
            c=self.mapping[frozenset(s)]
            if c=='#':
                self.numeric=True
                continue
            if self.numeric:
                if c=='J':
                    self.numeric=False
                    continue
                elif c=='K':
                    l.append('0')
                else:
                    l.append(chr(ord(c))-16)
            else:
                l.append(c)
        return l
