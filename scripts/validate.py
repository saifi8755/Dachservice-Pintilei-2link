from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re
root=Path(__file__).resolve().parents[1]/'dist'
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
errors=[];count=0
for f in root.rglob('*.html'):
 text=f.read_text();p=Parser();p.feed(text);tags=p.tags;count+=1
 for tag,attribute,value in [('h1',None,None),('title',None,None),('meta','name','description'),('link','rel','canonical')]:
  if len([a for t,a in tags if t==tag and (not attribute or a.get(attribute)==value)])!=1:errors.append(f'{f}: expected one {tag} {value}')
 ids=[a['id'] for _,a in tags if 'id' in a]
 if len(ids)!=len(set(ids)):errors.append(f'{f}: duplicate IDs')
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text):json.loads(block)
 for tag,a in tags:
  for key in ['src','href']:
   if key not in a:continue
   url=a[key];u=urlsplit(url)
   if u.scheme or u.netloc:continue
   if u.path:
    target=root/u.path.lstrip('/')
    if u.path.endswith('/'):target=target/'index.html'
    if not target.exists():errors.append(f'{f}: missing {url}')
   elif u.fragment and u.fragment not in ids:errors.append(f'{f}: missing #{u.fragment}')
  if tag=='img':
   if not all(a.get(k) for k in ['alt','width','height','loading','srcset']):errors.append(f'{f}: image metadata')
   for candidate in a.get('srcset','').split(','):
    if not (root/candidate.strip().split()[0].lstrip('/')).exists():errors.append('missing responsive image')
  if tag in ['input','select','textarea'] and a.get('type')!='checkbox':
   if not any(t=='label' and l.get('for')==a.get('id') for t,l in tags):errors.append(f'{f}: unlabeled field')
assert not errors,'\n'.join(errors)
print(f'PASS: {count} pages; local links, images, metadata, JSON-LD, IDs and form labels valid.')
print('CSS + JS:',sum((root/'assets'/x).stat().st_size for x in ['style.css','site.js']),'bytes uncompressed')
print('All image variants:',sum(x.stat().st_size for x in root.rglob('*.webp')),'bytes')
