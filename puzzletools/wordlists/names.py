'''
Generates lists of common American first names, using the Social Security
Administration's baby name data
'''

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO, TextIOWrapper
from puzzletools.wordlists.util import WordlistGenerator
import argparse, os

def load():
    req=urlopen('https://www.ssa.gov/oact/babynames/names.zip')
    return ZipFile(BytesIO(req.read()))

def read_names(z):
    both = WordlistGenerator()
    female = WordlistGenerator()
    male = WordlistGenerator()
    for n in z.namelist():
        if n.endswith('.txt'):
            with z.open(n,'r') as f:
                for l in TextIOWrapper(f):
                    name,gen,num=l.split(',')
                    num=int(num)
                    both.add(name,num)
                    if gen=='F':
                        female.add(name,num)
                    if gen=='M':
                        male.add(name,num)
    return (both,female,male)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir',help='directory to which the lists should be saved (default is the current directory)',default='.')
    args=parser.parse_args()
    path=args.outdir+os.sep
    b,f,m=read_names(load())
    kwa={'cutoff':200,'eliminate_duplicate_slugs':False}
    b.write(path+'names_all.txt',**kwa)
    f.write(path+'names_female.txt',**kwa)
    m.write(path+'names_male.txt',**kwa)
