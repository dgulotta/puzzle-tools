'''
Encoder and decoder for Morse code.
'''

import re
import encoder_base

_dash_hyphen_re = re.compile('[\u2010\u2011\u2012\u2013\u2014\u2015\u2043\u2212\uff0d]')

def dash_to_hyphen(s):
    """
    Replaces various kinds of dash characters with hyphens.
    """
    return _dash_hyphen_re.sub('-',s)

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

morse_to_alpha = encoder_base.reverse_dict(alpha_to_morse)

class MorseEncoder(encoder_base.Encoder):
    '''
    Converts text to Morse code.

        >>> enc = MorseEncoder()
        >>> enc('hello')
        '.... . .-.. .-.. ---'
    '''

    def __init__(self,**kwargs):
        '''
        Keyword arguments:
        ``sep`` - Character separator.  Default is ' '.
        ``wsep`` - Word separator.  Default is '/'.
        ``nonalnum`` - If ``True``, then non-alphanumeric characters are converted to Morse
        code when possible.  Otherwise, all non-alphanumeric characters are ignored.
        The default is ``False``.
        '''
        self.nonalnum = kwargs.get('nonalnum',False)
        super(MorseEncoder,self).__init__(**kwargs)

    def translate_char(self,s):
        if self.nonalnum or s.isalnum():
            return alpha_to_morse.get(s.upper())
        else:
            return None

class MorseDecoder(encoder_base.Decoder):
    '''
    Converts Morse code to text.

        >>> dec = MorseDecoder()
        >>> dec('-- --- .-. ... . / -.-. --- -.. .')
        'MORSE CODE'
    '''

    def translate_char(self,s):
        return morse_to_alpha[s]
