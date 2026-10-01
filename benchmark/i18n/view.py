import sys,re
f=sys.argv[1]; L=open(f,encoding='utf-8').read().splitlines()
bs=next(i for i,l in enumerate(L) if '<body' in l)
for i,l in enumerate(L[:bs],1):
    if re.search(r'<title|<meta (name|property)="(description|og:|twitter:)|<html',l): print(i,l)
skip=re.compile(r'^\s*<(symbol|path|circle|stop|rect|linearGradient|radialGradient|use|g |/g|line |defs|/defs|animate)')
insc=False
for i,l in enumerate(L[bs:],bs+1):
    if '<script>' in l: insc=True
    if insc and not (re.search(r'[^\x00-\x7f]',l) or 'hu-HU' in l or re.search(r"'[A-Za-z][^']{12,}'",l)): continue
    if skip.match(l) and not re.search(r'[^\x00-\x7f]',l): continue
    print(i,l)
