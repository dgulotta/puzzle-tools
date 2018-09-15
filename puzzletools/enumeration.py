import attr

class EnumerationMeta(type):

    def __new__(cls,name,bases,dct):
        c = super().__new__(cls,name,bases,dct)
        return attr.s(auto_attribs=True)(c)

    def __init__(cls,name,bases,dct):
        super().__init__(name,bases,dct)
        cls._set_items([])

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __contains__(self):
        return item in self.items

    def __reversed__(self):
        return reversed(self.items)

    def set_items_lazy(self, fn):
        self._item_loader = fn

    def _get_items(self):
        if not self._items and self._item_loader:
            self._items = self._item_loader()
        return self._items

    def _set_items(self, items):
        self._items = items
        self._item_loader = None

    items = property(_get_items, _set_items)
