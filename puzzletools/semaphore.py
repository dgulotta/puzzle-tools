from puzzletools import encoder_base

directions_unicode = list('\u2192\u2197\u2191\u2196\u2190\u2199\u2193\u2198')
directions_phonepad = list('63214789')
directions_numpad = list('69874123')
directions_rogue = list('LUKYHBJN')
directions_compass = 'E NE N NW W SW S SE'.split(' ')
directions_cartesian = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]

def convert_direction(d,from_rep,to_rep):
    return to_rep[from_rep.index(d)]

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

semaphore_to_alpha = encoder_base.reverse_dict(alpha_to_semaphore)

class SemaphoreEncoder(encoder_base.Encoder):
    '''encodes text to semaphore.

        >>> enc = SemaphoreEncoder(output_mode=directions_rogue)
        >>> print enc('hello')
        'HB JU BU BU HY'
    '''    

    def __init__(self,**kwargs):
        '''
        Keyword arguments:
        ``sep`` - Character separator.  Default is ' '.
        ``wsep`` - Word separator.  Default is '/'.
        ``output_mode`` - The representation of semaphore directions.   Supported input modes include:
        * ``directions_numpad`` - represents directions by numpad keys (down left = 1, down = 2, etc)
        * ``directions_phonepad`` - represents directions by telephone pad keys (up left = 1, up = 2, etc)
        * ``directions_rogue`` - represents directions by Rogue keys (left = h, down = j, etc)
        * ``directions_unicode`` (default) - represents directions by Unicode arrow characters (left = U+2190, up = U+2191, etc)
        In addition, you can specify a custom input mode as a list of 8 characters.
        The direction characters should be listed in counterclockwise order starting
        with right.
        '''
        o = kwargs.get('output_mode',directions_unicode)
        self.mapping = { k : ''.join(o[directions_unicode.index(c)] for c in v) for k,v in alpha_to_semaphore.items() }
        super(SemaphoreEncoder,self).__init__(**kwargs)

    def __call__(self,s):
        self.numeric = False
        return super(SemaphoreEncoder,self).__call__(s)

    def translate_char(self,s):
        if s.isnumeric():
            if s=='0':
                c=self.mapping['K']
            else:
                c=self.mapping[chr(ord(s)+16)]
            if self.numeric:
                return c
            else:
                self.numeric = True
                return (self.mapping['#'],c)
        else:
            c=self.mapping.get(s.upper())
            if c is None:
                return None
            if self.numeric:
                self.numeric = False
                return (self.mapping['J'],c)
            else:
                return c

class SemaphoreDecoder(encoder_base.Decoder):
    '''
    Decodes text from semaphore.
    
        >>> dec = SemaphoreDecoder(input_mode=directions_numpad)
        >>> print dec('62 19 21 23 / 34 29 61 21 48 41 47 64 29')
        FLAG SEMAPHORE
    '''

    def __init__(self,**kwargs):
        '''
        Keyword arguments:
        ``sep`` - Character separator.  Default is ' '.
        ``wsep`` - Word separator.  Default is '/'.
        ``input_mode`` - The representation of semaphore directions.   The representations are the
        same as for ``SemaphoreEncoder``.  The default is ``directions_numpad``.
        '''
        i = kwargs.get('input_mode',directions_numpad)
        self.mapping = { frozenset(i[directions_unicode.index(c)] for c in k) : v for k,v in semaphore_to_alpha.items() }
        super(SemaphoreDecoder,self).__init__(**kwargs)

    def __call__(self,s):
        self.numeric = False
        return super(SemaphoreDecoder,self).__call__(s)

    def translate_char(self,s):
        c = self.mapping[frozenset(s)]
        if c=='#':
            self.numeric = True
            return ''
        if self.numeric:
            if c=='J':
                self.numeric = False
                return ''
            elif c=='K':
                return '0'
            else:
                return chr(ord(c)-16)
        else:
            return c
