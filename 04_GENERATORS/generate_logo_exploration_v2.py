from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/naskah-visuals/logo_exploration_v2")
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(r"C:/Users/Digitalisasi/AppData/Local/hermes/profiles/content/fonts/Poppins")

NAVY = "#071726"
NAVY2 = "#0B2238"
CREAM = "#F5F2EB"
ORANGE = "#E85929"
INK = "#0B131D"
SLATE = "#71808E"

S = 720

def poly(draw, pts, fill):
    draw.polygon([(int(x), int(y)) for x,y in pts], fill=fill)

def line(draw, pts, fill, width, joint="curve"):
    draw.line([(int(x), int(y)) for x,y in pts], fill=fill, width=width, joint=joint)

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(int(v) for v in box), radius=int(radius), fill=fill, outline=outline, width=width)

def ellipse(draw, box, fill):
    draw.ellipse(tuple(int(v) for v in box), fill=fill)

def make(bg=None):
    return Image.new("RGBA", (S,S), bg if bg else (0,0,0,0))

# 01 - PAGE FOLD N: a single editorial N with a visible page corner fold.
def c01(bg= None):
    im=make(bg); d=ImageDraw.Draw(im)
    cream = CREAM if bg==NAVY else NAVY
    orange=ORANGE
    # heavy N silhouette
    left,right,top,bottom=160,560,140,580
    sw=86
    rounded(d,(left,top,left+sw,bottom),32,cream)
    rounded(d,(right-sw,top,right,bottom),32,cream)
    poly(d,[(left+sw-12,top),(left+sw+54,top),(right, bottom-10),(right-66,bottom-10)],cream)
    # page fold cut/accent at upper right, integrated into the letter body
    poly(d,[(right-sw,top),(right,top),(right-sw,top+88)],orange)
    # small cream cut within fold
    poly(d,[(right-sw+18,top+18),(right-18,top+18),(right-sw+18,top+68)],cream)
    return im

# 02 - NEGATIVE SPACE WINDOW: cream slab where the N is cut through as negative space.
def c02(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    slab = CREAM if bg==NAVY else NAVY
    hole = NAVY if bg==NAVY else CREAM
    rounded(d,(150,120,570,600),42,slab)
    # negative-space N cutout: vertical holes + diagonal hole, exposing background
    poly(d,[(235,180),(305,180),(485,520),(415,520)],hole)
    poly(d,[(220,180),(220,540),(280,540),(280,180)],hole)
    poly(d,[(440,180),(440,540),(500,540),(500,180)],hole)
    # orange page edge/registration mark, kept within the single monogram
    poly(d,[(510,120),(570,120),(570,180),(510,180)],ORANGE)
    return im

# 03 - CROSSOVER RIBBON: a continuous orange ribbon crosses two navy stems.
def c03(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    stem=CREAM if bg==NAVY else NAVY
    rounded(d,(165,155,250,575),42,stem)
    rounded(d,(470,155,555,575),42,stem)
    # ribbon with tapered ends, optical crossover
    poly(d,[(225,172),(292,172),(500,548),(433,548)],ORANGE)
    # little overlap seams to make the crossover feel designed, not assembled
    line(d,[(254,220),(286,220)],NAVY if bg==NAVY else CREAM,6)
    line(d,[(438,500),(470,500)],NAVY if bg==NAVY else CREAM,6)
    return im

# 04 - MARGIN N: a text-editorial mark; N is interrupted by a marginal vertical rule.
def c04(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    # offset, almost typographic N
    line(d,[(205,565),(205,155),(515,565),(515,155)],col,72)
    # editorial margin rail and a notch of accent
    line(d,[(130,155),(130,565)],ORANGE,14)
    line(d,[(130,155),(170,155)],ORANGE,14)
    line(d,[(130,565),(170,565)],ORANGE,14)
    # mask diagonal intersections slightly for an intentional printing-like gap
    return im

# 05 - INK STROKE: one continuous hand-drawn monoline, not a geometric block.
def c05(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=ORANGE if bg==NAVY else NAVY
    # smooth N-like single stroke with round joints (draw line + circles)
    pts=[(205,545),(205,180),(515,545),(515,180)]
    line(d,pts,col,50)
    for x,y in pts:
        ellipse(d,(x-25,y-25,x+25,y+25),col)
    # tiny editorial cut in the lower-left terminal: makes it authored
    cut = NAVY if bg==NAVY else CREAM
    poly(d,[(180,545),(215,545),(205,570)],cut)
    return im

# 06 - OPEN BOOK N: N is formed by two page planes, with the center valley implied.
def c06(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    acc=ORANGE
    # left page and right page as two folded panels; negative gap stays visible
    poly(d,[(170,170),(250,170),(360,360),(250,550),(170,550),(280,360)],col)
    poly(d,[(470,170),(550,170),(440,360),(550,550),(470,550),(360,360)],col)
    # spine is a narrow orange wedge, not a separate icon
    poly(d,[(352,345),(368,345),(384,375),(368,405),(352,405),(336,375)],acc)
    return im

# 07 - STENCIL CUT N: compact stencil with two purposeful bridges, highly scalable.
def c07(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    cut= NAVY if bg==NAVY else CREAM
    # thick N body
    poly(d,[(170,150),(270,150),(450,500),(450,150),(550,150),(550,570),(450,570),(270,230),(270,570),(170,570)],col)
    # stencil cuts on diagonal, one large and one small, using background color
    poly(d,[(286,230),(320,285),(320,350),(286,300)],cut)
    poly(d,[(400,410),(430,462),(430,520),(400,468)],cut)
    # one warm registration bar makes it recognizable at small size
    rounded(d,(150,130,205,185),16,ORANGE)
    return im

# 08 - PAPERCLIP N: an N made from a looped, continuous outline; academic stationery cue without drawing a paperclip.
def c08(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=ORANGE if bg==NAVY else NAVY
    # continuous outlined ribbon, rounded
    pts=[(215,550),(215,190),(515,550),(515,190)]
    line(d,pts,col,34)
    # offset interior hairline gives a paper/ink feel
    line(d,[(242,490),(242,260),(488,490),(488,260)],CREAM if bg==NAVY else NAVY,7)
    for x,y in [(215,550),(215,190),(515,550),(515,190)]:
        ellipse(d,(x-17,y-17,x+17,y+17),col)
    return im

# 09 - CITATION BRACKET N: squared bracket ends echo references and marginal citations.
def c09(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    # N with open bracket terminations, not rounded pills
    line(d,[(190,560),(190,160),(520,560),(520,160)],col,58)
    # bracket cuts at each terminal
    acc=ORANGE
    line(d,[(145,160),(190,160),(190,205)],acc,15)
    line(d,[(520,515),(520,560),(565,560)],acc,15)
    return im

# 10 - FOLDED RIBBON N: two-tone fold creates an N with a memorable mid-turn.
def c10(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    base=CREAM if bg==NAVY else NAVY
    # base N
    poly(d,[(170,160),(250,160),(470,515),(470,160),(550,160),(550,570),(470,570),(250,215),(250,570),(170,570)],base)
    # folded orange flap at center-right
    poly(d,[(342,340),(400,440),(470,515),(430,515),(342,415)],ORANGE)
    # small darker seam
    seam = NAVY2 if bg==NAVY else CREAM
    line(d,[(342,340),(400,440)],seam,8)
    return im

# 11 - TOP-CUT N: silhouette whose top-right corner is cut like a page, strong in avatar size.
def c11(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    # full N silhouette
    poly(d,[(170,150),(270,150),(450,500),(450,150),(550,150),(550,570),(450,570),(270,220),(270,570),(170,570)],col)
    # cut top right into a page corner, revealing background + orange under-sheet
    cut= NAVY if bg==NAVY else CREAM
    poly(d,[(450,150),(550,150),(550,220),(500,220)],cut)
    poly(d,[(450,150),(500,150),(500,185),(450,185)],ORANGE)
    return im

# 12 - ORBITAL N: mostly typographic, with a single enclosing arc that becomes part of the N.
def c12(bg=None):
    im=make(bg); d=ImageDraw.Draw(im)
    col=CREAM if bg==NAVY else NAVY
    acc=ORANGE
    # N body reduced to allow an arc to carry the personality
    line(d,[(225,535),(225,190),(500,535),(500,190)],col,62)
    # purposeful open arc, not a circle icon
    d.arc((130,110,595,610),start=300,end=110,fill=acc,width=18)
    # accent endpoint is squared, like a printed mark
    line(d,[(545,170),(565,145)],acc,18)
    return im

CONCEPTS=[
    ("01", "Page Fold", "N + one page-corner fold" , c01),
    ("02", "Negative Window", "N appears as a cutout" , c02),
    ("03", "Crossover Ribbon", "One ribbon crosses the N" , c03),
    ("04", "Margin Rule", "Editorial margin becomes the cue" , c04),
    ("05", "Ink Stroke", "One authored monoline gesture" , c05),
    ("06", "Open Book", "Two pages imply the N" , c06),
    ("07", "Stencil Cut", "Built for tiny avatar sizes" , c07),
    ("08", "Paperclip Line", "Continuous outline / stationery feel" , c08),
    ("09", "Citation Bracket", "Reference-mark geometry" , c09),
    ("10", "Folded Ribbon", "N with a mid-turn fold" , c10),
    ("11", "Page Cut", "Top corner becomes signature" , c11),
    ("12", "Open Orbit", "Typographic N + open arc" , c12),
]

# export transparent master and two presentation variants per concept
for num,name,desc,fn in CONCEPTS:
    master=fn(None)
    master.save(OUT/f"concept_{num}_{name.lower().replace(' ','_')}_transparent.png")
    fn(NAVY).convert("RGB").save(OUT/f"concept_{num}_{name.lower().replace(' ','_')}_navy.png")
    fn(CREAM).convert("RGB").save(OUT/f"concept_{num}_{name.lower().replace(' ','_')}_cream.png")

# Board with 12 different visual grammars
BW,BH=2200,3000
board=Image.new("RGB",(BW,BH),"#06121E")
d=ImageDraw.Draw(board)
ftitle=ImageFont.truetype(str(FONT_DIR/"Poppins-ExtraBold.ttf"),58)
fsub=ImageFont.truetype(str(FONT_DIR/"Poppins-Medium.ttf"),28)
flabel=ImageFont.truetype(str(FONT_DIR/"Poppins-Bold.ttf"),32)
fdesc=ImageFont.truetype(str(FONT_DIR/"Poppins-Regular.ttf"),22)
d.text((1100,64),"NASKAH.FK — N MONOGRAM EXPLORATION",font=ftitle,fill=CREAM,anchor="ma")
d.text((1100,135),"12 different shape ideas • reference-led • one letter only",font=fsub,fill=ORANGE,anchor="ma")

card_w,card_h=930,760
positions=[]
for row in range(4):
    for col in range(3):
        positions.append((100+col*1000,260+row*680))

for (num,name,desc,fn),(x,y) in zip(CONCEPTS,positions):
    bg=CREAM if (int(num)%2==0) else NAVY
    card=fn(bg).convert("RGB").resize((500,500),Image.Resampling.LANCZOS)
    # card background (keeps consistent board rhythm)
    d.rounded_rectangle((x,y,x+card_w,y+card_h),radius=28,fill="#0A2032",outline="#173A52",width=2)
    # small presentation tile, alternating
    tile_x=x+35;tile_y=y+35
    d.rounded_rectangle((tile_x,tile_y,tile_x+500,tile_y+500),radius=16,fill=bg)
    board.paste(card,(tile_x,tile_y))
    d.text((x+575,y+80),f"{num}  {name.upper()}",font=flabel,fill=CREAM)
    # word-wrap description
    words=desc.split(); cur=""; lines=[]
    for word in words:
        test=(cur+" "+word).strip()
        if d.textbbox((0,0),test,font=fdesc)[2] <= 280:
            cur=test
        else:
            lines.append(cur);cur=word
    if cur: lines.append(cur)
    for i,line_txt in enumerate(lines):
        d.text((x+575,y+140+i*34),line_txt,font=fdesc,fill="#A7B2BD")
    d.text((x+575,y+280),"simple N / no wordmark",font=fdesc,fill=ORANGE)

# Footer note
d.text((1100,3000-90),"Palette: Deep Navy • Cream • one warm accent | Generate SVG only after one direction is selected",font=fsub,fill="#92A1AF",anchor="mm")
board.save(OUT/"N_MONOGRAM_EXPLORATION_BOARD.png",quality=95)

# contact sheet at tiny scale to test avatar legibility
small=Image.new("RGB",(1440,1100),CREAM)
ds=ImageDraw.Draw(small)
ds.text((720,40),"AVATAR TEST — 96px",font=ftitle,fill=NAVY,anchor="ma")
for idx,(num,name,desc,fn) in enumerate(CONCEPTS):
    x=80+(idx%6)*220;y=170+(idx//6)*400
    tile=fn(NAVY).convert("RGB").resize((180,180),Image.Resampling.LANCZOS)
    small.paste(tile,(x,y))
    ds.text((x+90,y+205),num,font=flabel,fill=NAVY,anchor="ma")
    ds.text((x+90,y+245),name,font=fdesc,fill=INK,anchor="ma")
small.save(OUT/"N_MONOGRAM_AVATAR_TEST.png",quality=95)

print(f"Generated {len(CONCEPTS)*3} concept renders + 2 boards in {OUT}")
