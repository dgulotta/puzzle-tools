'''
Utilities for working with nucleotide and amino acid sequences.
'''

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

class AminoSequence(object):
    '''
    Represents a sequence of amino acids.

        >>> a = AminoSequence('ASDF')
        >>> a.long_form()
        ['ALA', 'SER', 'ASP', 'PHE']
        >>> AminoSequence.from_long_form('ALA SER ASP PHE')
        AminoSequence('ASDF')
    '''

    amino_acids = (
        # normal amino acids
        ('A' , 'ALA'),
        ('C' , 'CYS'),
        ('D' , 'ASP'),
        ('E' , 'GLU'),
        ('F' , 'PHE'),
        ('G' , 'GLY'),
        ('H' , 'HIS'),
        ('I' , 'ILE'),
        ('K' , 'LYS'),
        ('L' , 'LEU'),
        ('M' , 'MET'),
        ('N' , 'ASN'),
        ('P' , 'PRO'),
        ('Q' , 'GLN'),
        ('R' , 'ARG'),
        ('S' , 'SER'),
        ('T' , 'THR'),
        ('V' , 'VAL'),
        ('W' , 'TRP'),
        ('Y' , 'TYR'),
        # special amino acids
        ('U' , 'SEC'),
        ('O' , 'PYL'),
        # wildcards
        ('B' , 'ASX'),
        ('Z' , 'GLX'),
        ('J' , 'XLE'),
        ('X' , 'XAA'),
        # stop codon
        ('#' , '###')
    )

    one_to_three = dict(amino_acids)
    three_to_one = dict(map(reversed,amino_acids))

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

genetic_code_tmp = (
    ('UUU' , 'PHE'),
    ('UUC' , 'PHE'),
    ('UUA' , 'LEU'),
    ('UUG' , 'LEU'),
    ('UCU' , 'SER'),
    ('UCC' , 'SER'),
    ('UCA' , 'SER'),
    ('UCG' , 'SER'),
    ('UAU' , 'TYR'),
    ('UAC' , 'TYR'),
    ('UAA' , '###'),
    ('UAG' , '###'),
    ('UGU' , 'CYS'),
    ('UGC' , 'CYS'),
    ('UGA' , '###'),
    ('UGG' , 'TRP'),
    ('CUU' , 'LEU'),
    ('CUC' , 'LEU'),
    ('CUA' , 'LEU'),
    ('CUG' , 'LEU'),
    ('CCU' , 'PRO'),
    ('CCC' , 'PRO'),
    ('CCA' , 'PRO'),
    ('CCG' , 'PRO'),
    ('CAU' , 'HIS'),
    ('CAC' , 'HIS'),
    ('CAA' , 'GLN'),
    ('CAG' , 'GLN'),
    ('CGU' , 'ARG'),
    ('CGC' , 'ARG'),
    ('CGA' , 'ARG'),
    ('CGG' , 'ARG'),
    ('AUU' , 'ILE'),
    ('AUC' , 'ILE'),
    ('AUA' , 'ILE'),
    ('AUG' , 'MET'),
    ('ACU' , 'THR'),
    ('ACC' , 'THR'),
    ('ACA' , 'THR'),
    ('ACG' , 'THR'),
    ('AAU' , 'ASN'),
    ('AAC' , 'ASN'),
    ('AAA' , 'LYS'),
    ('AAG' , 'LYS'),
    ('AGU' , 'SER'),
    ('AGC' , 'SER'),
    ('AGA' , 'ARG'),
    ('AGG' , 'ARG'),
    ('GUU' , 'VAL'),
    ('GUC' , 'VAL'),
    ('GUA' , 'VAL'),
    ('GUG' , 'VAL'),
    ('GCU' , 'ALA'),
    ('GCC' , 'ALA'),
    ('GCA' , 'ALA'),
    ('GCG' , 'ALA'),
    ('GAU' , 'ASP'),
    ('GAC' , 'ASP'),
    ('GAA' , 'GLU'),
    ('GAG' , 'GLU'),
    ('GGU' , 'GLY'),
    ('GGC' , 'GLY'),
    ('GGA' , 'GLY'),
    ('GGG' , 'GLY'),
)

genetic_code = {x[0].replace('U','T') : AminoSequence.three_to_one[x[1]] for x in genetic_code_tmp}

del genetic_code_tmp
