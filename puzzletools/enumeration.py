class EnumerationMeta(type):

    def __new__(cls,name,bases,dct):
        newbases = list(bases)
        if 'display_key' in dct:
            newbases.append(_DisplayKey)
        newbases.append(_Dir)
        return super().__new__(cls,name,tuple(newbases),dct)

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

class _DisplayKey:
    def _display(self):
        return getattr(self,type(self).display_key)

    def __str__(self):
        return self._display()

    def __repr__(self):
        return '< {} {} >'.format(type(self).__name__,self._display())

class _Dir:
    def __dir__(self):
        items = super().__dir__()
        return [i for i in items if i in self.__dict__ or i.startswith('__')
            or callable(getattr(self,i))]
