class EnumerationMeta(type):

    def __new__(cls,name,bases,dct):
        if 'display_key' in dct:
            dk = dct['display_key']
            def __str__(self):
                return getattr(self,dk)
            dct.setdefault('__str__',__str__)
            def __repr__(self):
                return '< %s %s >'%(name,getattr(self,dk))
            dct.setdefault('__repr__',__repr__)
            def values(self):
                return {fld : getattr(self,fld) for fld in self.fields}
            dct.setdefault('values',values)
        return super().__new__(cls,name,bases,dct)

    def __init__(cls,name,bases,dct):
        super().__init__(name,bases,dct)
        if 'fields' in dct and 'data' in dct:
            cls.items=[cls(*d) for d in cls.data]
            cls.items_extended = cls.items+[cls(*d) for d in getattr(cls,'data_extra',[])]

    def by_field(self,field_name,extras=False):
        l = self.items_extended if extras else self.items
        return { getattr(v,field_name) : v for v in l }

    def __call__(self,*args):
        obj = type.__call__(self)
        for k,v in zip(self.fields,args):
            setattr(obj,k,v)
        return obj

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __contains__(self,item):
        return item in self.items

    def __reversed__(self):
        return reversed(self.items)
