"""Parametric, Fusion-importable enclosure using CadQuery. Units: mm.
Run: python cad/generate_enclosure.py
Actual PCB sizes and button switch geometry MUST be measured before final printing.
"""
from pathlib import Path
import cadquery as cq

ROOT=Path(__file__).resolve().parents[1]
STL=ROOT/'stl'; CAD=ROOT/'cad'
STL.mkdir(exist_ok=True)
W,H=142.0,210.0
T=3.0
DEPTH=34.0
CORNER=5.0
SCREWS=[(8,8),(W-8,8),(8,H-8),(W-8,H-8)]
BUTTONS=[('POWER',95,89),('BACK',120,89),('PRESS',95,62),('STOP',120,62)]

def base_box(w,h,d,z0=0):
    return cq.Workplane('XY').box(w,h,d,centered=(True,True,False)).translate((W/2,H/2,z0))

def rect_hole(obj,x,y,w,h,z=-1,depth=50):
    tool=cq.Workplane('XY').box(w,h,depth,centered=(True,True,False)).translate((x,y,z))
    return obj.cut(tool)

def circle_hole(obj,x,y,diam,z=-1,depth=50):
    tool=cq.Workplane('XY').center(x,y).circle(diam/2).extrude(depth).translate((0,0,z))
    return obj.cut(tool)

def engraved(obj,s,x,y,size,depth=.55):
    # cut away from the outward (+Z) face; fonts require FreeType available.
    try:
        tool=cq.Workplane('XY').text(s,size,depth, font='DejaVu Sans',kind='bold',halign='center',valign='center',combine=True).translate((x,y,T-depth+.05))
        return obj.cut(tool)
    except Exception as e:
        print('font engraving failed',s,e)
        return obj

# Faceplate: front surface z=3, back z=0
front=base_box(W,H,T).edges('|Z').fillet(CORNER)
front=rect_hole(front,71,166,36,44)
front=rect_hole(front,71,118,66,17)
front=circle_hole(front,39,79,18.2)
for label,x,y in BUTTONS:
    front=rect_hole(front,x,y,12.6,12.6)
    front=engraved(front,label,x,y+10.6,3.2,.4)
# piezo grille, not a large opening
for dx,dy in [(-6,0),(-3,0),(0,0),(3,0),(6,0),(-4.5,4),(0,4),(4.5,4),(-4.5,-4),(0,-4),(4.5,-4),(0,8),(0,-8)]:
    front=circle_hole(front,39+dx,42+dy,1.8)
# main screws M3 clearance, countersink via counterbores
for x,y in SCREWS:
    front=circle_hole(front,x,y,3.3)
    front=circle_hole(front,x,y,6.0,z=1.5,depth=2)
# LCD mounting holes (nominal common 75x31 pattern, verify)
for x in (71-37.5,71+37.5):
    for y in (118-15.5,118+15.5):
        front=circle_hole(front,x,y,2.7)
# Generic TFT retaining tie slots: not claimed to match module screws
for x in (47,95):
    for y in (139,194):
        front=rect_hole(front,x,y,2.3,5.0)
front=engraved(front,'COMPUTER',71,25,6.4,.65)
front=engraved(front,'DIRECTORY',71,15,6.1,.65)
front=engraved(front,'RFID / NETWORK CONSOLE',71,203,3.2,.35) if False else front

# Rear tub, closed back plate on bed, open top.
rear=base_box(W,H,DEPTH).edges('|Z').fillet(CORNER)
inner=base_box(W-5.6,H-5.6,DEPTH+3,z0=2.8)
rear=rear.cut(inner)
# Four screw-post cylinders (join walls), with blind holes
for x,y in SCREWS:
    post=cq.Workplane('XY').center(x,y).circle(5.4).extrude(DEPTH-2.8).translate((0,0,2.8))
    rear=rear.union(post)
    rear=circle_hole(rear,x,y,2.6,z=DEPTH-15.5,depth=17)
# Bottom-wall USB service notch: model dependent, enlarged for cable clearance
rear=rect_hole(rear,71,0,13,13,z=9,depth=11)
# SD card access notch on right wall
rear=rect_hole(rear,W,150,10,18,z=12,depth=8)
# simple internal anchor posts for generic tie-downs
for x,y in [(19,21),(123,21),(19,179),(123,179)]:
    boss=cq.Workplane('XY').center(x,y).circle(4.8).extrude(7).translate((0,0,2.8))
    rear=rear.union(boss)
    rear=circle_hole(rear,x,y,2.2,z=5,depth=6)
# vent slots in rear floor, lower middle so keep away from display modules
for y in (46,51,56):
    for x in (64,73,82):
        rear=rect_hole(rear,x,y,4,1.8,z=-1,depth=5)

# Optional color trim bezel for 12x12 square cap, not a functioning pushbutton.
bezel=cq.Workplane('XY').box(17.4,17.4,1.8,centered=(True,True,False))
bezel=bezel.cut(cq.Workplane('XY').box(12.8,12.8,4,centered=(True,True,False)).translate((0,0,-1)))

models={'front_panel':front,'rear_shell':rear,'square_button_trim':bezel}
for name,part in models.items():
    print('export',name)
    cq.exporters.export(part,str(STL/(name+'.stl')),exportType='STL',tolerance=0.075,angularTolerance=0.12)
    cq.exporters.export(part,str(CAD/(name+'.step')),exportType='STEP')
# Named multi-solid assembly for Fusion, with front panel and optional trims installed.
assm=cq.Assembly(name='Computer_Directory_Console')
assm.add(rear,name='RearShell',color=cq.Color(0.15,0.32,0.33))
assm.add(front,name='FrontPanel',loc=cq.Location(cq.Vector(0,0,DEPTH)),color=cq.Color(0.19,0.41,0.39))
for label,x,y in BUTTONS:
    rgb={'POWER':(0.78,0.16,0.20),'BACK':(0.96,0.69,0.1),'PRESS':(0.12,0.66,0.35),'STOP':(0.14,0.40,0.84)}[label]
    assm.add(bezel,name=label+'_Trim',loc=cq.Location(cq.Vector(x,y,DEPTH+T)),color=cq.Color(*rgb))
assm.save(str(CAD/'Console_Assembly.step'))
print('done')
