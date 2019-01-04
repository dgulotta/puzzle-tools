import cattr
import codecs
import datetime
import pkg_resources

def _parse_date(s, cl):
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()

_conv = cattr.Converter()
_conv.register_structure_hook(datetime.date, _parse_date)

def load_tsv(filename, ty=None):
    with pkg_resources.resource_stream(__name__, 'data/' + filename) as f:
        gen = (l.strip('\r\n').split('\t') for l in codecs.getreader('utf-8')(f))
        if ty is None:
            return list(gen)
        else:
            return [_conv.structure_attrs_fromtuple(row, ty) for row in gen]
