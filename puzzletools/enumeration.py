class EnumerationMeta(type):
    def __init__(cls,name,bases,dct):
        super(EnumerationMeta,cls).__init__(name,bases,dct)
        if hasattr(cls,'fields') and hasattr(cls,'data'):
            cls.items=[cls(*d) for d in cls.data]
            for f in cls.fields:
                setattr(cls,'by_'+f,{ getattr(v,f) : v for v in cls.items })

    def __call__(self,*args):
        obj = type.__call__(self)
        for k,v in zip(self.fields,args):
            setattr(obj,k,v)
        return obj
