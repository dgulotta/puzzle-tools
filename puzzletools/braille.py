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

    >>> braille_converter('binary','english')(int('011001',2))
    'D'
    >>> braille_converter('unicode','binary')('\u2819')
    25
    >>> braille_converter('english','binary')('D')
    25
    >>> grid = [[1,0,0,1],[0,0,1,0],[0,0,1,0]]
    >>> l2e = braille_converter('list','english')
    >>> [l2e(l) for l in braille_divide_grid(grid)]
    ['A', 'S']
    >>> grid[0][2] = None
    >>> [braille_possible_letters(*braille_list_to_binary_mask(l)) for l in braille_divide_grid(grid)]
    [['A'], ['P', 'S']]
'''

braille_alphabet = '\u2801\u2803\u2809\u2819\u2811\u280b\u281b\u2813\u280a\u281a\u2805\u2807\u280d\u281d\u2815\u280f\u281f\u2817\u280e\u281e\u2825\u2827\u283a\u282d\u283d\u2835'
braille_binary = [ord(ch)-0x2800 for ch in braille_alphabet]

braille_representations = ['binary','english','list','unicode']

def braille_converter(from_rep,to_rep):
    '''
    Returns a function that converts from the Braille representation
    ``from_rep`` to the Braille representation ``to_rep``
    '''
    if from_rep==to_rep:
        return lambda x : x
    if from_rep=='binary':
        if to_rep=='english':
            return braille_binary_to_english
        elif to_rep=='list':
            return braille_binary_to_list
        elif to_rep=='unicode':
            return braille_binary_to_unicode
        else:
            raise ValueError('Invalid braille representation %s'%to_rep)
    elif to_rep=='binary':
        if from_rep=='english':
            return braille_english_to_binary
        elif from_rep=='list':
            return braille_list_to_binary
        elif from_rep=='unicode':
            return braille_unicode_to_binary
        else:
            raise ValueError('Invalid braille representation %s'%from_rep)
    else:
        return lambda x, f1=braille_converter(from_rep,'binary'), f2=braille_converter('binary',to_rep): f2(f1(x))

def _braille_validate_binary(s):
    if s<0 or s>=0x100:
        raise ValueError('Invalid binary Braille sequence')

def braille_binary_to_unicode(code):
    _braille_validate_binary(code)
    return chr(0x2800+code)

def braille_binary_to_english(code):
    _braille_validate_binary(code)
    return chr(0x41+braille_binary.index(code))

def braille_binary_to_list(code):
    _braille_validate_binary(code)
    return [(code>>i)&1 for i in range(6)]

def braille_english_to_binary(ch):
    i = ord(ch)-0x41
    if i<0 or i>=26:
        raise ValueError("Invalid English letter")
    return braille_binary[i]

def braille_unicode_to_binary(br):
    i = ord(br)-0x2800
    if i<0 or i>=0x100:
        raise ValueError("Invalid Braille unicode character")
    return i

def braille_list_to_binary(l):
    if len(l)!=6 and len(l)!=8:
        raise ValueError("Invalid Braille list length")
    return sum(bool(l[i])<<i for i in range(len(l)))

def braille_possible_letters(code,mask):
    '''
    Returns the possible letters for a Braille block for which we have partial
    knowledge.

    Parameters:
    code - the binary representation of the dots that are known to be raised
    mask - the binary representation of the dots that are known
    '''
    return [braille_binary_to_english(i) for i in braille_binary if i&mask==code&mask]

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
    return (braille_list_to_binary(l),sum((l[i] is not None)<<i for i in range(6)))
