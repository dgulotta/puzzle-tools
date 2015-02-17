'''
A script for generating a list of movies, tv shows, actors, and directors from
text files provided by IMDb.

The script can either download the IMDb text files from one of the ftp mirrors
or use a local copy.  If you want to download the files yourself, they can be
found at at http://www.imdb.com/interfaces#plain.
The files that are used by this script are actors, actresses, aka-titles,
and directors, and ratings.

Example usage:
To download the files from an ftp server and generate all of the lists in the
current directory, run
python imdb.py --ftp
'''

from puzzletools.wordlist_util import WordlistGenerator, normalize_alnum
import codecs, gzip, math, re, io, ftplib
import argparse, random

class LocalOpener:
    def __init__(self,path):
        self.path=path

    def __call__(self,s):
        fn='%s/%s.list'%(self.path,s)
        try:
            return codecs.open(fn,'r','iso-8859-1')
        except FileNotFoundError:
            pass
        return gzip.open(fn+'.gz','rt',encoding='iso-8859-1')

class FTPOpener:
    def __init__(self,site,path):
        self.site=site
        self.path=path

    def __call__(self,s):
        f = io.BytesIO()
        with ftplib.FTP(self.site) as ftp:
            ftp.login()
            ftp.cwd(self.path)
            ftp.retrbinary("RETR %s.list.gz"%s,f.write)
        f.seek(0)
        return codecs.getreader('iso-8859-1')(gzip.GzipFile(fileobj=f,mode='rb'))

class IMDb:

    _name_re = re.compile(r'^(.*?)(?:, (.*?))?(?: \(.*?\))?$')
    _ratings_re = re.compile(r'^ {6}[0-9.*]{10} +(\d+) +\d?\d\.\d  (.*)$')
    _actors_re = re.compile(r'^(.*?)\t+(.*?)(?:  \[(.*?)\])?(?:  <(\d+)>)?$')
    _directors_re = re.compile(r'^(.*?)\t+(.*?)(?:  .*)?$')
    _aka_re = re.compile(r'^   \(aka (.*)\)\s+\(USA\)(?: \(short title\))?(?: \(imdb display title\))?$')
    _ftp_sites = [
        ('ftp.fu-berlin.de','/pub/misc/movies/database/'),
        ('ftp.funet.fi','/pub/mirrors/ftp.imdb.com/pub/'),
        ('ftp.sunet.se','/pub/tv+movies/imdb/'),
    ]

    def __init__(self,opener,odir):
        self.counts = {}
        self.open=opener
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
        actors = WordlistGenerator()
        for s in ('actors','actresses'):
            with self.open(s) as f:
                self.skip_header(f,'----\t')
                for l in f:
                    try:
                        g = self._actors_re.match(l).groups()
                        if g[0]:
                            name = self.parse_name(g[0])
                        if g[3]:
                            actors.add(name,int(self.weights[int(g[3])-1]*self.counts[g[1]]))
                    except(AttributeError, IndexError, KeyError):
                        pass
        self.write_list('imdb_actors.txt',actors,8000)

    def do_movies(self):
        movies = WordlistGenerator()
        tv = WordlistGenerator()
        def add_count(k,v):
            if k.startswith('"'):
                if k.find('{')==-1:
                    d = tv
                else:
                    return
            else:
                d = movies
            d.add(self.parse_movie(k),v,max)
        for k,v in self.counts.items():
            add_count(k,v)
        with self.open('aka-titles') as f:
            self.skip_header(f,'====')
            for l in f:
                try:
                    if len(l)>1:
                        if l.startswith(' '):
                            if count>=1200:
                                g = self._aka_re.match(l).groups()
                                add_count(g[0],count)
                        else:
                            count = self.counts.get(l.strip(),0)
                except(AttributeError, KeyError):
                    pass
        self.write_list('imdb_movies.txt',movies,4000)
        self.write_list('imdb_tv.txt',tv,1200)

    def do_directors(self):
        directors = WordlistGenerator()
        with self.open('directors') as f:
            self.skip_header(f,'----\t')
            for l in f:
                try:
                    g = self._directors_re.match(l).groups()
                    if g[0]:
                        name = self.parse_name(g[0])
                    if g[1]:
                        directors.add(name,self.counts[g[1]])
                except(AttributeError, KeyError):
                    pass
        self.write_list('imdb_directors.txt',directors,8000)

    def write_list(self,name,d,cutoff):
        d.write('%s/%s'%(self.odir,name),cutoff)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument('--indir',help='get data files from the given local directory')
    inputs.add_argument('--ftp',help='get data files from an ftp mirror',action='store_true')
    parser.add_argument('--outdir',help='directory to which the lists should be saved (default is the current directory)',default='.')
    parser.add_argument('--actors',help='generate a list of actors (if no lists are specified, all will be generated)',action='store_true')
    parser.add_argument('--directors',help='generate a list of directors',action='store_true')
    parser.add_argument('--movies',help='generate lists of movies and tv shows',action='store_true')
    args = parser.parse_args()
    if args.indir is not None:
        opener = LocalOpener(args.indir)
    elif args.ftp:
        opener = FTPOpener(*random.choice(IMDb._ftp_sites))
    else:
        parser.error('either --indir or --ftp is required')
    if not (args.actors or args.directors or args.movies):
        args.actors=True
        args.directors=True
        args.movies=True
    i = IMDb(opener,args.outdir)
    i.load_counts()
    if args.movies:
        i.do_movies()
    if args.directors:
        i.do_directors()
    if args.actors:
        i.do_actors()
