# ================================================================
#  Makes the animated banner assets/header.svg
#  Header only (name glitch, no subtitle). Run:  python make-banner.py
#  Needs:      pip install fonttools
# ================================================================
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
HERE=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(HERE,'..','assets')
F=TTFont(os.path.join(HERE,'DotGothic16.woff'))
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
NAME='SPEYVENERABLE'; ns=116; nls=5
nw=width(NAME,ns,nls); nx=(W-nw)/2; ny=236
name_d=path(NAME,ns,nx,ny,nls)
tag_d=path('/PROFILE',30,30,50)
title_d=path('Hello, World...',26,0,0)
tw=width('Hello, World...',26)
title_d=path('Hello, World...',26,(W+330-tw)/2+60,48)
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
<clipPath id="slice"><rect x="0" width="{W}" height="22" y="162"><animate attributeName="y" dur="5s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;.30;.32;.34;.36;.68;.70;.72;.74;1" values="162;142;187;132;172;197;137;177;152;162"/></rect></clipPath>
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
print(len(svg), nw)

