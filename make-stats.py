# Builds assets/stats.svg = FOLLOWERS / STARS / REPOS for your GitHub account.
# Stars are summed over every public repo you own (forks not counted).
# Runs automatically in GitHub Actions (.github/workflows/stats.yml).
# Manual run:  GH_USER=Speyvenerable python make-stats.py     (needs: pip install fonttools)
import os, json, urllib.request
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

USER=os.environ.get('GH_USER','Speyvenerable')
TOKEN=os.environ.get('GITHUB_TOKEN','')
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','assets','stats.svg')

def api(url):
    h={'Accept':'application/vnd.github+json','User-Agent':'stats'}
    if TOKEN: h['Authorization']='Bearer '+TOKEN
    return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=30))

try:
    followers=api(f'https://api.github.com/users/{USER}')['followers']
    stars=repos=0; page=1
    while True:
        batch=api(f'https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}')
        if not batch: break
        for r in batch:
            if r.get('fork'): continue
            repos+=1; stars+=r.get('stargazers_count',0)
        if len(batch)<100: break
        page+=1
except Exception as e:
    print('API failed:',e); raise SystemExit(1)
print(USER,'followers',followers,'stars',stars,'repos',repos)

F=TTFont(os.path.join(HERE,'DotGothic16.woff'))
gs=F.getGlyphSet(); cmap=F.getBestCmap(); UPM=F['head'].unitsPerEm; hmtx=F['hmtx']
def width(t,s,ls=0): return sum(hmtx[cmap[ord(c)]][0]*s/UPM+ls for c in t)-ls
def path(t,s,x,y,ls=0):
    k=s/UPM; pen=SVGPathPen(gs); cx=x
    for c in t:
        g=cmap.get(ord(c))
        if g is None: continue
        gs[g].draw(TransformPen(pen,(k,0,0,-k,cx,y))); cx+=hmtx[g][0]*k+ls
    return pen.getCommands()

W,H=1000,190
tiles=[('FOLLOWERS',followers),('STARS',stars),('REPOS',repos)]
tw=(W-18-2*14)/3
parts=[]
for i,(lab,val) in enumerate(tiles):
    x=9+i*(tw+14); v=str(val)
    vw=width(v,70,3); lw=width(lab,22,2)
    parts.append(f'''<g transform="translate({x:.1f},9)">
<rect width="{tw:.1f}" height="{H-18}" fill="#0d2250" stroke="#1f6fe6" stroke-width="3"/>
<rect width="{tw:.1f}" height="38" fill="#14306a"/><rect y="38" width="{tw:.1f}" height="1.5" fill="#fff" opacity=".35"/>
<path d="{path(lab,22,(tw-lw)/2,27,2)}" fill="#cfe0ff"/>
<path d="{path(v,70,(tw-vw)/2,128,3)}" fill="#2f7bff" opacity=".8" filter="url(#bl)"/>
<path class="n" style="animation-delay:{i*.4}s" d="{path(v,70,(tw-vw)/2,128,3)}" fill="#fff"/>
<g fill="none" stroke="#fff" stroke-width="2"><path d="M8 46h10M8 46v9"/><path d="M{tw-8:.1f} {H-26}h-10M{tw-8:.1f} {H-26}v-9"/></g></g>''')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{USER}: {followers} followers, {stars} stars, {repos} repos">
<style>@keyframes n{{0%,100%{{opacity:1}}50%{{opacity:.78}}}}.n{{animation:n 3s ease-in-out infinite}}@keyframes sc{{0%{{transform:translateY(-50px)}}100%{{transform:translateY(200px)}}}}.sc{{animation:sc 5s linear infinite}}</style>
<defs><filter id="bl" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
<pattern id="s" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".28"/></pattern>
<linearGradient id="sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa0ff" stop-opacity="0"/><stop offset=".5" stop-color="#7db8ff" stop-opacity=".2"/><stop offset="1" stop-color="#5aa0ff" stop-opacity="0"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="#020812"/>
{''.join(parts)}
<rect width="{W}" height="{H}" fill="url(#s)"/>
<rect class="sc" width="{W}" height="50" fill="url(#sb)"/>
<rect x="2.5" y="2.5" width="{W-5}" height="{H-5}" fill="none" stroke="#1f6fe6" stroke-width="5"/>
</svg>'''
open(OUT,'w').write(svg)
