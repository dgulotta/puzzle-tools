def reverse_dict(d):
    return {v:k for k,v in d.items()}

class Encoder:

    def __init__(self,**kwargs):
        self.sep=kwargs.get('sep',' ')
        self.wsep=kwargs.get('wsep','/')

    def __call__(self,s):
        l = []
        for c in s:
            t = self.translate_char(c)
            if t is None:
                if len(l)==0 or l[-1]!=self.wsep:
                    l.append(self.wsep)
            elif isinstance(t,str):
                l.append(t)
            else:
                l.extend(t)
        return self.sep.join(l)

class Decoder:

    def __init__(self,**kwargs):
        self.sep=kwargs.get('sep',' ')
        self.wsep=kwargs.get('wsep','/')

    def __call__(self,s):
        l=s.split(self.sep)
        return ''.join(' ' if c==self.wsep else self.translate_char(c) for c in l)
