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

_dash_hyphen_re = re.compile('[\u2010\u2011\u2012\u2013\u2014\u2015\u2043\u2212\uff0d]')

def dash_to_hyphen(s):
    """
    Replaces various kinds of dash characters with hyphens.
    """
    return _dash_hyphen_re.sub('-',s)

class Morse(Code):

    alpha_to_morse = {
        'A' : '.-',
        'B' : '-...',
        'C' : '-.-.',
        'D' : '-..',
        'E' : '.',
        'F' : '..-.',
        'G' : '--.',
        'H' : '....',
        'I' : '..',
        'J' : '.---',
        'K' : '-.-',
        'L' : '.-..',
        'M' : '--',
        'N' : '-.',
        'O' : '---',
        'P' : '.--.',
        'Q' : '--.-',
        'R' : '.-.',
        'S' : '...',
        'T' : '-',
        'U' : '..-',
        'V' : '...-',
        'W' : '.--',
        'X' : '-..-',
        'Y' : '-.--',
        'Z' : '--..',
        '0' : '-----',
        '1' : '.----',
        '2' : '..---',
        '3' : '...--',
        '4' : '....-',
        '5' : '.....',
        '6' : '-....',
        '7' : '--...',
        '8' : '---..',
        '9' : '----.',
        '.' : '.-.-.-',
        ',' : '--..--',
        ':' : '---...',
        '?' : '..--..',
        "'" : '.----.',
        '-' : '-....-',
        '/' : '-..-.',
        '(' : '-.--.',
        ')' : '-.--.-',
        '"' : '.-..-.',
        '=' : '-...-',
        '+' : '.-.-.',
        '@' : '.--.-.',
        '\u00d7' : '-..-'
    }

    morse_to_alpha = reverse_dict(alpha_to_morse)

    to_parent = morse_to_alpha.__getitem__
    from_parent = alpha_to_morse.__getitem__
