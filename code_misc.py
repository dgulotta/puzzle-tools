def alphabet_to_time_zone(c):
    """
    Given a time zone (in the form of a UTC offset), returns the corresponding
    letter
    """
    n = ord(c.upper())-0x40
    if n<=0 or n>26:
        raise ValueError('Invalid letter')
    if n<=9:
        return n
    elif n==10:
        return None
    elif n<=13:
        return n-1
    elif n<=25:
        return 13-n
    else:
        return 0

def time_zone_to_alphabet(n):
    """
    Given a letter, returns the UTC offset of the corresponding military time
    zone
    """
    if n<-12 or n>12:
        raise ValueError('Invalid time zone')
    if n<0:
        return chr(0x4d-n)
    elif n==0:
        return 'Z'
    elif n<=9:
        return chr(0x40+n)
    else:
        return chr(0x41+n)
