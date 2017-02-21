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

    alpha_to_semaphore = {
        'A' : frozenset('\u2199\u2193'),
        'B' : frozenset('\u2193\u2190'),
        'C' : frozenset('\u2193\u2196'),
        'D' : frozenset('\u2191\u2193'),
        'E' : frozenset('\u2197\u2193'),
        'F' : frozenset('\u2193\u2192'),
        'G' : frozenset('\u2198\u2193'),
        'H' : frozenset('\u2199\u2190'),
        'I' : frozenset('\u2199\u2196'),
        'J' : frozenset('\u2191\u2192'),
        'K' : frozenset('\u2199\u2191'),
        'L' : frozenset('\u2199\u2197'),
        'M' : frozenset('\u2199\u2192'),
        'N' : frozenset('\u2199\u2198'),
        'O' : frozenset('\u2190\u2196'),
        'P' : frozenset('\u2191\u2190'),
        'Q' : frozenset('\u2197\u2190'),
        'R' : frozenset('\u2190\u2192'),
        'S' : frozenset('\u2198\u2190'),
        'T' : frozenset('\u2191\u2196'),
        'U' : frozenset('\u2197\u2196'),
        'V' : frozenset('\u2191\u2198'),
        'W' : frozenset('\u2197\u2192'),
        'X' : frozenset('\u2197\u2198'),
        'Y' : frozenset('\u2196\u2192'),
        'Z' : frozenset('\u2198\u2192'),
        '#' : frozenset('\u2197\u2191'),
        '\b' : frozenset('\u2198\u2196'),
    }

    def __init__(self,dirs=DirectionUnicode):
        self.mapping = { k : ''.join(dirs.from_parent(c) for c in sorted(v)) for k,v in self.alpha_to_semaphore.items() }
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

    semaphore_to_alpha = reverse_dict(StatefulSemaphoreEncoder.alpha_to_semaphore)

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
