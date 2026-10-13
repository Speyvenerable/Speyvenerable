"""
Makes the animated images for the GitHub profile README (assets/*.svg).

HOW TO USE
  1. Change the words in the CONFIG block below (NAME, SUBTITLE, etc).
  2. Install the one thing it needs (only once):   pip install fonttools
  3. Run it from this folder:                       python make_profile_images.py
  4. Upload the new files inside ../assets to your GitHub repo (replace the old ones).

The text is turned into shapes using the DotGothic16 font (the same pixel font as the
portfolio), so GitHub shows it correctly. Use only normal letters, numbers and common
symbols. The middle dot used between words is typed as the "·" character.
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
FONT = os.path.join(HERE, 'DotGothic16.woff')

# ===================== CONFIG: change these =====================
NAME      = 'SPEYVENERABLE'                                  # big glitch name
SUBTITLE  = 'UI/UX DESIGNER  ·  NOVEL READER  ·  GAMER'      # typing line under the name
TAG       = '/PROFILE'                                       # box at the top-left
TOPTITLE  = 'Hello, World...'                                # text at the top of the banner
SECTIONS  = [('about', '/ABOUT', 'who am i...'),
             ('projects', '/PROJECTS', 'things i made...'),
             ('contact', '/CONTACT', 'find me here...'),
             ('views', '/VIEWS', 'who stopped by...')]
BUTTONS   = [('btn-portfolio', 'PORTFOLIO'), ('btn-epubreader', 'EPUBREADER'),
             ('btn-discord', 'DISCORD'), ('btn-gmail', 'GMAIL')]
# =================================================================
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
F=TTFont(FONT)
gs=F.getGlyphSet(); cmap=F.getBestCmap(); UPM=F['head'].unitsPerEm; hmtx=F['hmtx']
def width(text,size,ls=0):
    return sum(hmtx[cmap[ord(c)]][0]*size/UPM+ls for c in text)-ls
def path(text,size,x,y,ls=0):
    s=size/UPM; pen=SVGPathPen(gs); cx=x
    for c in text:
        g=cmap.get(ord(c)); 
        if g is None: continue
        tp=TransformPen(pen,(s,0,0,-s,cx,y)); gs[g].draw(tp)
        cx+=hmtx[g][0]*s+ls
    return pen.getCommands()
def advances(text,size,ls=0):
    out=[0];cx=0
    for c in text:
        cx+=hmtx[cmap[ord(c)]][0]*size/UPM+ls; out.append(cx)
    return out

W,H=1000,340
ns=116; nls=5
nw=width(NAME,ns,nls)
while nw>900 and ns>30:
    ns-=2; nw=width(NAME,ns,nls)
nx=(W-nw)/2; ny=222
name_d=path(NAME,ns,nx,ny,nls)
SUB=SUBTITLE
ss=26; sls=2; sw=width(SUB,ss,sls)
while sw>900 and ss>12:
    ss-=1; sw=width(SUB,ss,sls)
sx=(W-sw)/2; sy=272
sub_d=path(SUB,ss,sx,sy,sls)
adv=advances(SUB,ss,sls)
tag_d=path(TAG,30,30,50)
tw=width(TOPTITLE,26)
title_d=path(TOPTITLE,26,(W+330-tw)/2+60,48)
n=len(SUB)
# typing steps: cumulative widths
xs=[sx+a for a in adv]
vals_w=';'.join(f'{round(a,1)}' for a in adv)
vals_cx=';'.join(f'{round(sx+a,1)}' for a in adv)
# timeline: dur 9s. typing 0.8s..3.8s then hold, erase at 8.6
keyT=[0]; 
steps=len(adv)
import numpy as np
times=[0.1+ (3.2*i/(steps-1)) /9 for i in range(steps)]
kt=';'.join(f'{t:.4f}' for t in [0]+times+[0.93,1])
vw=';'.join(['0']+[f'{sx+a:.1f}' for a in adv]+[f'{sx+adv[-1]:.1f}','0'])
vc=';'.join([f'{sx:.1f}']+[f'{sx+a:.1f}' for a in adv]+[f'{sx+adv[-1]:.1f}',f'{sx:.1f}'])
# glitch timing (dur 5s): bursts at ~ .30-.36 and .70-.74
def anim(name,frames):
    return f'@keyframes {name}{{{frames}}}'
css=f'''
.nm{{transform-box:fill-box}}
@keyframes gr{{0%,28%,38%,66%,76%,100%{{transform:translate(0,0)}}30%{{transform:translate(-9px,2px)}}32%{{transform:translate(7px,-3px)}}34%{{transform:translate(-5px,1px)}}36%{{transform:translate(4px,0)}}68%{{transform:translate(8px,-2px)}}70%{{transform:translate(-7px,2px)}}72%{{transform:translate(3px,0)}}74%{{transform:translate(-2px,0)}}}}
@keyframes gc{{0%,28%,38%,66%,76%,100%{{transform:translate(0,0)}}30%{{transform:translate(9px,-2px)}}32%{{transform:translate(-7px,3px)}}34%{{transform:translate(5px,-1px)}}36%{{transform:translate(-4px,0)}}68%{{transform:translate(-8px,2px)}}70%{{transform:translate(7px,-2px)}}72%{{transform:translate(-3px,0)}}74%{{transform:translate(2px,0)}}}}
@keyframes gm{{0%,28%,38%,66%,76%,100%{{transform:translate(0,0)}}31%{{transform:translate(-3px,0)}}33%{{transform:translate(3px,1px)}}35%{{transform:translate(-2px,0)}}69%{{transform:translate(3px,0)}}71%{{transform:translate(-3px,-1px)}}}}
@keyframes gv{{0%,29%,37%,67%,75%,100%{{opacity:0}}30%,33%,36%{{opacity:1}}31%,34%{{opacity:.2}}68%,70%,72%,74%{{opacity:1}}69%,71%,73%{{opacity:.2}}}}
@keyframes gtint{{0%,29%,37%,67%,75%,100%{{opacity:.0}}30%,33%,36%,68%,71%,74%{{opacity:.16}}}}
@keyframes scan{{0%{{transform:translateY(-60px)}}100%{{transform:translateY(360px)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes twinkle{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
@keyframes glow{{0%,100%{{filter:drop-shadow(0 0 4px #3a8bff)}}50%{{filter:drop-shadow(0 0 12px #5aa0ff)}}}}
@keyframes sweep{{0%{{transform:translateX(-300px)}}100%{{transform:translateX(1100px)}}}}
.r{{animation:gr 5s steps(1,end) infinite}}
.c{{animation:gc 5s steps(1,end) infinite}}
.m{{animation:gm 5s steps(1,end) infinite}}
.v{{animation:gv 5s steps(1,end) infinite}}
.tint{{animation:gtint 5s steps(1,end) infinite}}
.sc{{animation:scan 5.5s linear infinite}}
.bl{{animation:blink 1s steps(1,end) infinite}}
.tw{{animation:twinkle 2.6s ease-in-out infinite}}
.frame{{animation:glow 3.4s ease-in-out infinite}}
.sw{{animation:sweep 4.2s ease-in-out infinite}}
'''
tw_dots=''.join(f'<rect class="tw" x="{x}" y="{y}" width="4" height="4" fill="#7df9ff" style="animation-delay:{d}s"/>' for x,y,d in [(70,120,0),(930,140,.6),(120,300,1.1),(880,95,1.7),(60,215,2.2),(945,250,.3),(840,310,1.4),(180,105,.9)])
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Speyvenerable">
<title>Speyvenerable</title>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#06122a"/><stop offset="1" stop-color="#020812"/></linearGradient>
<radialGradient id="vg" cx="50%" cy="55%" r="65%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".65"/></radialGradient>
<linearGradient id="sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa0ff" stop-opacity="0"/><stop offset=".5" stop-color="#7db8ff" stop-opacity=".22"/><stop offset="1" stop-color="#5aa0ff" stop-opacity="0"/></linearGradient>
<linearGradient id="ul" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1f6fe6" stop-opacity="0"/><stop offset=".5" stop-color="#7db8ff"/><stop offset="1" stop-color="#1f6fe6" stop-opacity="0"/></linearGradient>
<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".28"/></pattern>
<filter id="bl" x="-10%" y="-60%" width="120%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="gl" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="cs"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
<clipPath id="slice"><rect x="0" width="{W}" height="22" y="150"><animate attributeName="y" dur="5s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.30;.32;.34;.36;.68;.70;.72;.74;1" values="150;130;175;120;160;185;125;165;140;150"/></rect></clipPath>
<clipPath id="type"><rect x="0" y="{sy-30}" height="44" width="0"><animate attributeName="width" dur="9s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vw}"/></rect></clipPath>
<clipPath id="inner"><rect x="9" y="9" width="{W-18}" height="{H-18}"/></clipPath>
</defs>
<style>{css}</style>
<rect width="{W}" height="{H}" fill="#000"/>
<g clip-path="url(#inner)">
<rect x="9" y="9" width="{W-18}" height="{H-18}" fill="url(#bg)"/>
<g opacity=".9">{tw_dots}</g>
<!-- header bar -->
<rect x="9" y="9" width="{W-18}" height="70" fill="#0d2250" opacity=".85"/>
<rect x="9" y="9" width="300" height="70" fill="#14306a" opacity=".9"/>
<rect x="9" y="78" width="{W-18}" height="1.5" fill="#fff" opacity=".35"/>
<rect x="309" y="9" width="1.5" height="70" fill="#fff" opacity=".35"/>
<path d="{tag_d}" fill="#fff" transform="translate(0,10)"/>
<rect x="340" y="38" width="16" height="16" fill="#1226ff"/><rect x="364" y="38" width="16" height="16" fill="#ff2a2a"/><rect x="388" y="38" width="16" height="16" fill="#1aff3a"/>
<path d="{title_d}" fill="#cfe0ff" opacity=".95"/>
<!-- name -->
<path d="{name_d}" fill="#2f7bff" opacity=".85" filter="url(#bl)"/>
<path class="r nm" d="{name_d}" fill="#ff2d55" style="mix-blend-mode:screen"/>
<path class="c nm" d="{name_d}" fill="#00f0ff" style="mix-blend-mode:screen"/>
<path class="m nm" d="{name_d}" fill="#ffffff"/>
<g clip-path="url(#slice)"><g class="v"><path d="{name_d}" fill="#7df9ff" transform="translate(18,0)"/></g></g>
<rect class="tint" x="9" y="80" width="{W-18}" height="{H-90}" fill="#ff2d55" opacity="0"/>
<!-- underline -->
<rect x="{nx}" y="{ny+16}" width="{nw}" height="3" fill="url(#ul)"/>
<rect class="sw" x="0" y="{ny+15}" width="120" height="5" fill="#fff" opacity=".55" style="mix-blend-mode:screen" clip-path="url(#cs)"/>
<!-- subtitle typing -->
<g clip-path="url(#type)"><path d="{sub_d}" fill="#cfe0ff"/></g>
<rect class="bl" x="{sx:.1f}" y="{sy-22}" width="12" height="24" fill="#7df9ff"><animate attributeName="x" dur="9s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vc}"/></rect>
<!-- scanlines / scan bar / vignette -->
<rect x="9" y="9" width="{W-18}" height="{H-18}" fill="url(#sl)"/>
<rect class="sc" x="9" y="0" width="{W-18}" height="60" fill="url(#sb)"/>
<rect x="9" y="9" width="{W-18}" height="{H-18}" fill="url(#vg)"/>
</g>
<!-- frame + corner brackets -->
<rect class="frame" x="4.5" y="4.5" width="{W-9}" height="{H-9}" fill="none" stroke="#1f6fe6" stroke-width="5"/>
<g fill="none" stroke="#fff" stroke-width="2.5"><path d="M22 96h22M22 96v22"/><path d="M{W-22} 96h-22M{W-22} 96v22"/><path d="M22 {H-22}h22M22 {H-22}v-22"/><path d="M{W-22} {H-22}h-22M{W-22} {H-22}v-22"/></g>
</svg>'''
open(os.path.join(OUT,'header.svg'),'w').write(svg)
print('header.svg written')

# ---- section bars ----
def bar(name,label,title,w=1000,h=64):
    td=path(label,30,28,43); tt=path(title,22,0,0)
    twid=width(title,22)
    ttd=path(title,22,w-60-twid,40)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
<style>@keyframes b{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}.d{{animation:b 2.4s ease-in-out infinite}}</style>
<defs><pattern id="s" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".25"/></pattern></defs>
<rect width="{w}" height="{h}" fill="#050f24"/>
<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="#0d2250" stroke="#1f6fe6" stroke-width="3"/>
<rect x="3" y="3" width="{twid_l(label)}" height="{h-6}" fill="#14306a"/>
<rect x="{twid_l(label)+3}" y="3" width="1.5" height="{h-6}" fill="#fff" opacity=".35"/>
<path d="{td}" fill="#fff"/>
<rect class="d" x="{twid_l(label)+30}" y="26" width="12" height="12" fill="#1226ff"/><rect class="d" style="animation-delay:.3s" x="{twid_l(label)+50}" y="26" width="12" height="12" fill="#ff2a2a"/><rect class="d" style="animation-delay:.6s" x="{twid_l(label)+70}" y="26" width="12" height="12" fill="#1aff3a"/>
<path d="{ttd}" fill="#cfe0ff"/>
<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="url(#s)"/>
<g fill="none" stroke="#fff" stroke-width="2"><path d="M10 10h12M10 10v10"/><path d="M{w-10} {h-10}h-12M{w-10} {h-10}v-10"/></g>
</svg>'''
def twid_l(label): return int(width(label,30))+56
for fn,lab,tit in SECTIONS:
    open(os.path.join(OUT,f'{fn}.svg'),'w').write(bar(fn,lab,tit))

# ---- buttons ----
def button(fn,label,color='#1f6fe6'):
    w=int(width(label,26,1))+110; h=60
    d=path(label,26,70,39,1)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
<style>@keyframes g{{0%,100%{{opacity:.6}}50%{{opacity:1}}}}.g{{animation:g 2.8s ease-in-out infinite}}</style>
<defs><filter id="f"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="s" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".25"/></pattern></defs>
<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="#12306a" stroke="#fff" stroke-opacity=".4"/>
<rect class="g" x="2" y="2" width="{w-4}" height="{h-4}" fill="none" stroke="{color}" stroke-width="2" filter="url(#f)"/>
<rect x="12" y="19" width="22" height="22" fill="none" stroke="#fff" stroke-width="2.4"/><rect x="19" y="26" width="8" height="8" fill="#7df9ff"/>
<path d="{d}" fill="#fff"/>
<rect x="3" y="3" width="{w-6}" height="{h-6}" fill="url(#s)"/>
<g fill="none" stroke="#fff" stroke-width="2"><path d="M8 8h10M8 8v9"/><path d="M{w-8} {h-8}h-10M{w-8} {h-8}v-9"/></g>
</svg>'''
for fn,lab in BUTTONS:
    open(os.path.join(OUT,f'{fn}.svg'),'w').write(button(fn,lab))
