'''
Encoder and decoder for Morse code.
    >>> from puzzletools.code import StringEncoder, StringDecoder
    >>> enc = StringEncoder(Morse)
    >>> enc('hello')
    '.... . .-.. .-.. ---'
    >>> dec = StringDecoder(Morse)
    >>> dec('-- --- .-. ... . / -.-. --- -.. .')
    'MORSE CODE'
'''

import re
from puzzletools.code import Code, reverse_dict
from puzzletools.datafiles import load_tsv

_dash_hyphen_re = re.compile('[\u2010\u2011\u2012\u2013\u2014\u2015\u2043\u2212\uff0d]')

def dash_to_hyphen(s):
    """
    Replaces various kinds of dash characters with hyphens.
    """
    return _dash_hyphen_re.sub('-',s)

class Morse(Code):

    alpha_to_morse = dict(load_tsv('morse.tsv'))
    morse_to_alpha = reverse_dict(alpha_to_morse)

    to_parent = morse_to_alpha.__getitem__
    from_parent = alpha_to_morse.__getitem__
