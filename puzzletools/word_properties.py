def is_cipher(w1,w2):
    '''
    Returns true if ``w1`` and ``w2`` are related by a substitution cipher.

        >>> is_cipher('oceanfront','asburypark')
        True
        >>> is_cipher('oceanfront','nineteenth')
        False
    '''
    if len(w1)!=len(w2):
        return False
    d1={}
    d2={}
    for c1,c2 in zip(w1,w2):
        if c1 in d1:
            if d1[c1]!=c2:
                return False
        else:
            d1[c1]=c2
        if c2 in d2:
            if d2[c2]!=c1:
                return False
        else:
            d2[c2]=c1
    return True

def is_sub_anagram(w1,w2):
    '''
    Returns true if ``w1`` can be formed by rearranging a subset of the
    letters of ``w2``.

        >>> is_sub_anagram('inches','cohesion')
        True
    '''
    return all(w2.count(c)>=w1.count(c) for c in set(w1))
