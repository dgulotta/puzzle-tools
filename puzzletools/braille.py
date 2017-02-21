'''
Utilities for working with Braille.

This module can represent Braille in two different ways:
either as Unicode characters, or in binary form.

The eight dots of extended Braille are numbered as follows:
``14``
``25``
``36``
``78``
Traditional Braille uses only the first six dots.
The letter D, for example, is represented by the
Braille pattern
``**``
``.*``
``..``
where stars represent raised dots.  Since dots
1,4,5 are raised, the binary representation is
011001, or 25 in base 10.

    >>> from puzzletools.code import CodeConverter, Alphabet
    >>> CodeConverter(BrailleBinary,Alphabet)(0b011001)
    'D'
    >>> CodeConverter(BrailleUnicode,BrailleBinary)('\u2819')
    25
    >>> CodeConverter(Alphabet,BrailleBinary)('D')
    25
    >>> grid = [[1,0,0,1],[0,0,1,0],[0,0,1,0]]
    >>> l2e = CodeConverter(BrailleList,Alphabet)
    >>> [l2e(l) for l in braille_divide_grid(grid)]
    ['A', 'S']
    >>> grid[0][2] = None
    >>> [braille_possible_letters(*braille_list_to_binary_mask(l)) for l in braille_divide_grid(grid)]
    [['A'], ['P', 'S']]
'''

from puzzletools.code import Code

braille_alphabet = '\u2801\u2803\u2809\u2819\u2811\u280b\u281b\u2813\u280a\u281a\u2805\u2807\u280d\u281d\u2815\u280f\u281f\u2817\u280e\u281e\u2825\u2827\u283a\u282d\u283d\u2835'
braille_binary = [ord(ch)-0x2800 for ch in braille_alphabet]

class BrailleBinary(Code):

    @staticmethod
    def validate(data):
        if data<0 or data>=0x100:
            raise ValueError("Invalid Braille")

    @staticmethod
    def from_parent(data):
        i = ord(data.upper())-0x41
        if i<0 or i>=26:
            raise ValueError("Invalid English letter")
        return braille_binary[i]

    @staticmethod
    def to_parent(data):
        return chr(0x41+braille_binary.index(data))

class BrailleUnicode(Code):

    parent = BrailleBinary
    list_constructor = ''.join

    @staticmethod
    def from_parent(data):
        return chr(0x2800+data)

    @staticmethod
    def to_parent(data):
        return ord(data)-0x2800

class BrailleList(Code):

    parent = BrailleBinary

    @staticmethod
    def to_parent(l):
        if len(l)!=6 and len(l)!=8:
            raise ValueError("Invalid Braille list length")
        return sum(bool(l[i])<<i for i in range(len(l)))

    @staticmethod
    def from_parent(code):
        return [(code>>i)&1 for i in range(6)]

def braille_possible_letters(code,mask):
    '''
    Returns the possible letters for a Braille block for which we have partial
    knowledge.

    Parameters:
    code - the binary representation of the dots that are known to be raised
    mask - the binary representation of the dots that are known
    '''
    return [BrailleBinary.to_parent(i) for i in braille_binary if i&mask==code&mask]

def braille_divide_grid(grid):
    '''
    Parses a grid into 3x2 blocks.  The grid should be input as a list of
    lists in column major format.

    The blocks are returned as six-element lists.
    '''
    return [[grid[y+j][x+i] for i in range(2) for j in range(3)] for y in range(0,len(grid),3) for x in range(0,len(grid[0]),2)]

def braille_list_to_binary_mask(l):
    '''
    Converts a six-item list of True/False/None values to a binary representation of a
    Braille character and a mask.  True represents a raised dot, False represents a lack
    of a dot, and None represents uncertainty.
    '''
    return (BrailleList.to_parent(l),sum((l[i] is not None)<<i for i in range(6)))
