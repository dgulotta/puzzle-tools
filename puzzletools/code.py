import abc

class Code(metaclass=abc.ABCMeta):

    @staticmethod
    def validate(data):
        pass

    @classmethod
    def ancestors(cls):
        anc = [cls]
        while(cls!=cls.parent):
            cls=cls.parent
            anc.append(cls)
        return anc

    list_constructor = list

    @staticmethod
    @abc.abstractmethod
    def to_parent(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def from_parent(self):
        pass

class Alphabet(Code):

    list_constructor = ''.join

    @staticmethod
    def to_parent(data):
        return data

    @staticmethod
    def from_parent(data):
        return data

Code.parent = Alphabet

class CodeConverter:

    @staticmethod
    def _find_ancestors(from_anc,to_anc):
        for fpos,a in enumerate(from_anc):
            try:
                tpos=to_anc.index(a)
                return (fpos,tpos)
            except ValueError:
                pass
        raise TypeError("Codes have no common ancestors")

    def __init__(self,from_code,to_code):
        from_anc = from_code.ancestors()
        to_anc = to_code.ancestors()
        fpos,tpos = self._find_ancestors(from_anc,to_anc)
        from_conv = [a.to_parent for a in from_anc[:fpos]]
        to_conv = [a.from_parent for a in to_anc[tpos-1::-1]] if tpos>0 else []
        self.from_code = from_code
        self.to_code = to_code
        self.converters = from_conv + to_conv

    def convert_one(self,value):
        for conv in self.converters:
            value = conv(value)
        return value

    def convert_many(self,value):
        gen = (self.convert_one(v) for v in value)
        return self.to_code.list_constructor(gen)

    def __call__(self,value):
        try:
            return self.convert_one(value)
        except:
            try:
                return self.convert_many(value)
            except:
                pass
            raise

def reverse_dict(d):
    return {v:k for k,v in d.items()}

def string_preprocess(c):
    if c.isalnum():
        return c.upper()
    else:
        return None

class StringEncoder:

    def __init__(self,code=None,sep=' ',wsep='/',pre=string_preprocess,encoder=None):
        """
        Keyword arguments:
        ``code`` - The code to use.  Can be ``None`` if ``encoder`` is
        specified.
        ``sep`` - Character separator..
        ``wsep`` - Word separator.
        ``pre`` - String preprocessing function.  The default one
        removes all non-alphanumeric characters and converts letters to
        uppercase.
        ``encoder`` - The function that does the encoding.  Not needed
        if ``code`` is specified.
        """
        self.sep=sep
        self.wsep=wsep
        self.pre=pre
        if encoder is None:
            if code is None:
                raise ValueError("Either 'encoder' or 'code' must be specified")
            else:
                self.encode = CodeConverter(Alphabet,code).convert_many
        else:
            self.encode = encoder

    def __call__(self,s):
        l = [[]]
        for c in s:
            ch = self.pre(c)
            if ch is None:
                if l[-1]:
                    l.append([])
            else:
                l[-1].append(ch)
        if not l[-1]:
            l.pop()
        bigwsep = self.sep+self.wsep+self.sep
        return bigwsep.join(self.sep.join(self.encode(w)) for w in l)

class StringDecoder:
    def __init__(self,code=None,sep=' ',wsep='/',decoder=None):
        """
        Keyword arguments:
        ``code`` - The code to use.  Can be ``None`` if ``decoder`` is
        specified.
        ``sep`` - Character separator.
        ``wsep`` - Word separator.
        ``decoder`` - The function that does the decoding.  Not needed
        if ``code`` is specified.
        """
        self.sep=sep
        self.wsep=wsep
        if decoder is None:
            if code is None:
                raise ValueError("Either 'decoder' or 'code' must be specified")
            else:
                self.decode = CodeConverter(code,Alphabet).convert_many
        else:
            self.decode = decoder

    def __call__(self,s):
        wds=s.split(self.wsep)
        return ' '.join(''.join(self.decode(w.strip(self.sep).split(self.sep))) for w in wds)
