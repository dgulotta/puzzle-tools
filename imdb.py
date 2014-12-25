'''
A script for generating a list of movies and actors from text files
provided by IMDb.

The IMDb text files can be found at http://www.imdb.com/interfaces#plain.
The files that are used by this script are actors, actresses, aka-titles,
and directors, and ratings.

To generate the lists, download the files and then run
python imdb.py [input_path] [output_path]
'''

from collections import defaultdict
from normalize import normalize_alnum
import codecs, gzip, math, re

class IMDb:

    _name_re = re.compile(r'^(.*?)(?:, (.*?))?(?: \(.*?\))?$')
    _ratings_re = re.compile(r'^ {6}[0-9.*]{10} +(\d+) +\d?\d\.\d  (.*)$')
    _actors_re = re.compile(r'^(.*?)\t+(.*?)(?:  \[(.*?)\])?(?:  <(\d+)>)?$')
    _directors_re = re.compile(r'^(.*?)\t+(.*?)(?:  .*)?$')
    _aka_re = re.compile(r'^   \(aka (.*)\)\s+\(USA\)(?: \(short title\))?(?: \(imdb display title\))?$')

    def __init__(self,idir=None,odir=None):
        self.counts = {}
        if idir is None:
            idir = '.'
        if odir is None:
            odir = idir
        self.idir = idir
        self.odir = odir
        self.weights = []
        f = math.exp(-.2)
        x = 1
        for i in range(75):
            self.weights.append(x)
            x*=f

    @staticmethod
    def parse_name(s):
        last, first = IMDb._name_re.match(s).groups()
        return normalize_alnum('%s %s'%(first,last))

    @staticmethod
    def parse_movie(s):
        return normalize_alnum(s[:s.find(' (')])

    def open(self,s):
        fn='%s/%s.list'%(self.idir,s)
        try:
            return codecs.open(fn,'r','iso-8859-1')
        except FileNotFoundError:
            pass
        return gzip.open(fn+'.gz','rt',encoding='iso-8859-1')

    def skip_header(self,f,s):
        for l in f:
            if l.startswith(s):
                return

    def load_counts(self):
        with self.open('ratings') as f:
            self.skip_header(f,'MOVIE RATINGS REPORT')
            self.skip_header(f,'New')
            for l in f:
                m = self._ratings_re.match(l)
                if m:
                    g = m.groups()
                    self.counts[g[1]]=int(g[0])

    def do_actors(self):
        actors = defaultdict(lambda : 0)
        for s in ('actors','actresses'):
            with self.open(s) as f:
                self.skip_header(f,'----\t')
                for l in f:
                    try:
                        g = self._actors_re.match(l).groups()
                        if g[0]:
                            name = self.parse_name(g[0])
                        if g[3]:
                            actors[name]+=int(self.weights[int(g[3])-1]*self.counts[g[1]])
                    except(AttributeError, IndexError, KeyError):
                        pass
        self.write_list('imdb_actors.txt',actors,8000)

    def do_movies(self):
        movies = defaultdict(lambda : 0)
        tv = defaultdict(lambda : 0)
        def add_count(k,v):
            if k.startswith('"'):
                if k.find('{')==-1:
                    d = tv
                else:
                    return
            else:
                d = movies
            d[self.parse_movie(k)]+=v
        for k,v in self.counts.items():
            add_count(k,v)
        with self.open('aka-titles') as f:
            self.skip_header(f,'====')
            for l in f:
                try:
                    if len(l)>1:
                        if l.startswith(' '):
                            g = self._aka_re.match(l).groups()
                            add_count(g[0],count)
                        else:
                            count = self.counts.get(l.strip(),0)
                except(AttributeError, KeyError):
                    pass
        self.write_list('imdb_movies.txt',movies,4000)
        self.write_list('imdb_tv.txt',tv,2000)

    def do_directors(self):
        directors = defaultdict(lambda : 0)
        with self.open('directors') as f:
            self.skip_header(f,'----\t')
            for l in f:
                try:
                    g = self._directors_re.match(l).groups()
                    if g[0]:
                        name = self.parse_name(g[0])
                    if g[1]:
                        directors[name]+=self.counts[g[1]]
                except(AttributeError, KeyError):
                    pass
        self.write_list('imdb_directors.txt',directors,8000)

    def write_list(self,name,d,cutoff):
        l = [(v,k) for k,v in d.items() if v>=cutoff]
        l.sort(reverse=True)
        with open('%s/%s'%(self.odir,name),'w') as f:
            for v, k in l:
                print("%s\t%d"%(k,v),file=f)

def usage():
    print("usage: imdb.py [input_path] [output_path]",file=sys.stderr)
    sys.exit(64)


if __name__=='__main__':
    import sys
    if len(sys.argv)>3:
        usage()
    i = IMDb(*sys.argv[1:])
    i.load_counts()
    i.do_movies()
    i.do_directors()
    i.do_actors()
