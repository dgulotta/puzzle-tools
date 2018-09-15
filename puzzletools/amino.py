'''
Utilities for working with nucleotide and amino acid sequences.
'''

from puzzletools.enumeration import EnumerationMeta
from puzzletools.code import Code
from puzzletools.datafiles import load_tsv
import re

def amino_encode(s):
    '''
    Convenience function for converting a DNA or RNA string into an amino
    acid sequence.
    '''
    return str(NucleotideSequence(s).to_amino())

base_pair={ 'A' : 'T', 'C' : 'G', 'G' : 'C', 'T' : 'A' }

def _groups_of_three(x):
    return (x[i:i+3] for i in range(0,len(x)-2,3))

class NucleotideSequence:
    '''
    A sequence of nucleotides.

        >>> n = NucleotideSequence('GATATCGCA')
        >>> n.dna_string()
        'GATATCGCA'
        >>> n.rna_string()
        'GAUAUCGCA'
        >>> n.conjugate()
        NucleotideSequence('TGCGATATC')
        >>> n[2:8]
        NucleotideSequence('TATCGC')
        >>> n.to_amino()
        AminoSequence('DIA')
        >>> n.to_amino().long_form()
        ['ASP', 'ILE', 'ALA']
    '''

    def __init__(self, seq):
        '''
        Creates a new nucleotide sequence.  seq may be either a string
        (both T's and U's are allowed) or another nucleotide sequence.
        '''
        if isinstance(seq, NucleotideSequence):
            self.nucleotides = seq.nucleotides
        else: 
            self.nucleotides = ''.join(seq).upper().replace('U','T')

    def conjugate(self):
        '''
        Returns the conjugate of this sequence.
        '''
        return type(self)(''.join(base_pair[i] for i in reversed(self.nucleotides)))

    def rna_string(self):
        return self.nucleotides.replace('T','U')

    def dna_string(self):
        return self.nucleotides

    def to_amino(self,start_behavior='keep'):
        """
        Convert this sequence to an amino acid sequence.

        Start behaviors:
        'keep' - Codes from the beginning to the string to the end of the string.
        'chop' - Codes from the beginning of the string to the end of the string.  Will discard a single leading Met and arbitrarily many trailing stop codons.
        'search' - Starts coding when it finds a start codon.  Stops if it encounters a stop codon.
        """
        if start_behavior!='keep' and start_behavior!='chop' and start_behavior!='search':
            raise ValueError('Unrecognized start behavior.  Allowed behaviors are keep, chop, search.')
        code = self.nucleotides
        if(start_behavior=='search'):
            offset = code.find('ATG')
            if offset!=-1:
                code = code[offset+3:]
            else:
                code = ''
        sequence = ''.join(genetic_code[i] for i in _groups_of_three(code))
        if(start_behavior=='search'):
            sequence = re.sub('#.*','',sequence)
        elif(start_behavior=='chop'):
            sequence = re.sub('^M','',sequence)
            sequence = re.sub('#*$','',sequence)
        return AminoSequence(sequence)

    def __getitem__(self, index):
        return NucleotideSequence(self.nucleotides[index])

    def __str__(self):
        return self.nucleotides

    def __repr__(self):
        return "NucleotideSequence(%s)"%repr(self.nucleotides)

class AminoAcid(metaclass=EnumerationMeta):
    letter: str
    abbr: str
    name: str

AminoAcid.items = load_tsv('amino.tsv', AminoAcid)

amino_acids_extended = AminoAcid.items + load_tsv('amino_extra.tsv', AminoAcid)

class AminoSequence(object):
    '''
    Represents a sequence of amino acids.

        >>> a = AminoSequence('ASDF')
        >>> a.long_form()
        ['ALA', 'SER', 'ASP', 'PHE']
        >>> AminoSequence.from_long_form('ALA SER ASP PHE')
        AminoSequence('ASDF')
    '''

    one_to_three = { v.letter : v.abbr.upper() for v in amino_acids_extended }
    three_to_one = { v.abbr.upper() : v.letter for v in amino_acids_extended }

    def __init__(self, seq):
        '''
        Constructs a new amino acid sequence.  seq can be either another amino
        acid sequence, or a string of one-letter amino acid abbreviations.
        '''
        if isinstance(seq, AminoSequence):
            self.acids = seq.acids
        else:
            self.acids = ''.join(seq).upper()

    def long_form(self):
        '''
        Returns the three letter abbreviations for the sequence of amino acids.
        '''
        return [self.one_to_three[i] for i in self.acids]

    def __str__(self):
        return self.acids

    def __repr__(self):
        return 'AminoSequence(%s)' % repr(self.acids)

    @staticmethod
    def from_long_form(seq):
        '''
        Converts a string or list of three-letter amino acid abbreviations into an AminoSequence.
        '''
        if isinstance(seq, str):
            seq = _groups_of_three(re.sub('[^A-Z]+','',seq.upper()))
        short_seq = ''.join(AminoSequence.three_to_one[i] for i in seq)
        return AminoSequence(short_seq)

class Amino(Code):

    to_parent=AminoSequence.three_to_one.__getitem__
    from_parent=AminoSequence.one_to_three.__getitem__

genetic_code = dict(load_tsv('genetic_code.tsv'))
