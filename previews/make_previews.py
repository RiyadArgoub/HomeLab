from pathlib import Path
from PIL import Image, ImageDraw,ImageFont,ImageOps
import svgwrite,cairosvg,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews';OUT.mkdir(exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(size,bold=False):return ImageFont.truetype(B if bold else F,size)
# Faceplate drawing with dimensions converted from print model (actual CAD 142x210)
S=4
im=Image.new('RGB',(900,1060),(15,24,34));d=ImageDraw.Draw(im)
origin=(175,70)
def p(x,y):return (origin[0]+x*S, origin[1]+(210-y)*S)
# enclosure silhouette
d.rounded_rectangle([p(0,210),p(142,0)],radius=18,fill=(36,62,69),outline=(95,137,140),width=4)
# mounting screws
for x in (8,134):
 for y in (8,202):
  px,py=p(x,y);d.ellipse((px-12,py-12,px+12,py+12),outline=(140,160,170),width=3)
# ST7789 opening and embedded image
cx,cy=p(71,166);ww,hh=36*S,44*S
box=[int(cx-ww/2),int(cy-hh/2),int(cx+ww/2),int(cy+hh/2)]
d.rounded_rectangle([box[0]-8,box[1]-8,box[2]+8,box[3]+8],radius=8,fill=(12,14,24))
photo=Image.open(ROOT/'assets/avatars/heather.png').convert('RGB').resize((ww,hh))
im.paste(photo,(box[0],box[1]));d.rectangle(box,outline=(118,207,204),width=3)
# 1602 character display
cx,cy=p(71,118);ww,hh=66*S,17*S
rect=(int(cx-ww/2),int(cy-hh/2),int(cx+ww/2),int(cy+hh/2))
d.rounded_rectangle(rect,radius=8,fill=(24,87,99),outline=(122,184,178),width=3)
d.text((rect[0]+8,rect[1]+10),'HEATHER-PC1',font=font(18,True),fill=(225,247,234))
d.text((rect[0]+8,rect[1]+36),'AI  ONLINE',font=font(16),fill=(225,247,234))
# joystick
cx,cy=p(39,79)
d.ellipse((cx-42,cy-42,cx+42,cy+42),fill=(26,29,36),outline=(110,131,147),width=4)
d.ellipse((cx-23,cy-23,cx+23,cy+23),fill=(92,97,107),outline=(162,171,188),width=3)
# buttons
for label,x,y,color in [('POWER',95,89,(195,57,66)),('BACK',120,89,(224,176,53)),('PRESS',95,62,(60,162,94)),('STOP',120,62,(59,126,201))]:
 px,py=p(x,y)
 d.rounded_rectangle((px-25,py-25,px+25,py+25),radius=7,fill=color,outline=(222,229,225),width=3)
 width=d.textbbox((0,0),label,font=font(12,True))[2]
 d.text((px-width/2,py-41),label,font=font(12,True),fill='white')
# buzzer grille
cx,cy=p(39,42)
for dx,dy in [(-6,0),(-3,0),(0,0),(3,0),(6,0),(-4.5,4),(0,4),(4.5,4),(-4.5,-4),(0,-4),(4.5,-4),(0,8),(0,-8)]:
 px,py=p(39+dx,42+dy);d.ellipse((px-4,py-4,px+4,py+4),fill=(11,20,24))
# brand
for txt,y,sz in [('COMPUTER',25,23),('DIRECTORY',15,22)]:
 px,py=p(71,y);bounds=d.textbbox((0,0),txt,font=font(sz,True));d.text((px-(bounds[2]-bounds[0])/2,py-sz/2),txt,font=font(sz,True),fill=(210,238,230))
d.text((42,13),'COMPUTER DIRECTORY   /   FRONT PANEL',font=font(25,True),fill=(235,242,247))
d.text((42,1022),'Concept preview • verify your actual TFT, LCD, joystick and button dimensions before printing',font=font(15),fill=(164,179,193))
im.save(OUT/'enclosure_front_preview.png')
# GUI/TFT screen mock-up (240x320 at 2x)
img=Image.new('RGB',(240,320),(9,14,22));q=ImageDraw.Draw(img)
q.rectangle((0,0,240,30),fill=(18,53,68))
q.text((10,7),'COMPUTER INFO',font=font(17,True),fill='white')
ph=Image.open(ROOT/'assets/avatars/heather.png').convert('RGB').resize((120,120))
img.paste(ph,(60,38))
q.text((12,172),'Heather-PC1',font=font(17,True),fill='white')
q.text((12,203),'ROLE: AI',font=font(12),fill=(161,211,225))
q.text((12,224),'STATUS: ONLINE',font=font(12),fill=(114,229,160))
q.text((12,252),'AI experiments and testing',font=font(10),fill=(210,217,230))
q.rectangle((0,297,240,320),fill=(20,32,44))
q.text((8,304),'GREEN: Wake  BLUE: Stop',font=font(10),fill=(125,220,228))
img.resize((480,640)).save(OUT/'display_heather_example.png')
# overview wiring diagram SVG cards: authoritative listed net map, NOT deceptive wire paths.
s=svgwrite.Drawing(str(ROOT/'schematics'/'wiring_overview.svg'),size=('1440px','1010px'),viewBox='0 0 1440 1010')
s.add(s.rect(insert=(0,0),size=('1440px','1010px'),fill='#0b1520'))
s.add(s.text('ESP32 COMPUTER DIRECTORY   /   PROTOTYPE WIRING',insert=(55,66),font_family='Arial',font_size=34,font_weight='bold',fill='#edf7f5'))
s.add(s.text('Module-level pin map • consistent with firmware • 3.3 V logic • not a routed PCB',insert=(57,101),font_family='Arial',font_size=17,fill='#aac1d0'))
cards=[
 ('ST7789V COLOR TFT','GPIO 23  →  DIN / MOSI\nGPIO 18  →  CLK / SCK\nGPIO 16  →  CS\nGPIO 17  →  DC\nGPIO 14  →  RST\n3V3  →  VCC*   GND → GND\nBL  →  VERIFY MODULE SPEC',60,142,'#53b6bc'),
 ('microSD SPI BREAKOUT','GPIO 23  →  MOSI / DI\nGPIO 18  →  SCK / CLK\nGPIO 19  ←  MISO / DO\nGPIO 13  →  CS\n3V3  →  VCC*\nGND  →  GND',518,142,'#c4a6e9'),
 ('1602 LCD + I2C','GPIO 21  ↔  SDA\nGPIO 22  →  SCL\nGND  →  GND\n3V3  →  VCC ONLY IF SUPPORTED\n5V BACKPACK: ADD I2C\nLEVEL SHIFTER + 5V SUPPLY',975,142,'#e0b972'),
 ('JOYSTICK ANALOG','GPIO 34  ←  VRx\nGPIO 35  ←  VRy\n3V3  →  VCC\nGND  →  GND\nSW  →  NOT CONNECTED',60,504,'#82ce99'),
 ('4 SQUARE BUTTONS','POWER RED  →  GPIO 32\nBACK YELLOW  →  GPIO 33\nPRESS GREEN  →  GPIO 25\nSTOP BLUE  →  GPIO 26\nOther terminal of each → GND\nINPUT_PULLUP in firmware',518,504,'#e9a2ae'),
 ('PASSIVE PIEZO','GPIO 27  →  Piezo (+)\nGND  →  Piezo (-)\nOnly small 3.3V-compatible piezo\nActive / high-current buzzers:\nADD a suitable transistor driver.',975,504,'#7ec5e8')]
for title,body,x,y,color in cards:
 s.add(s.rect(insert=(x,y),size=('407px','315px'),rx=18,fill='#152738',stroke='#456072',stroke_width=2))
 s.add(s.rect(insert=(x,y),size=('407px','9px'),rx=4,fill=color))
 s.add(s.text(title,insert=(x+22,y+45),font_family='Arial',font_size=23,font_weight='bold',fill=color))
 for i,line in enumerate(body.split('\n')):
  s.add(s.text(line,insert=(x+22,y+88+i*31),font_family='DejaVu Sans Mono',font_size=17,fill='#e2ecf3'))
s.add(s.text('Power: ESP32 via USB 5 V. Share GND. Do not connect 5 V signals to GPIO. Verify module pinouts before soldering.',insert=(58,885),font_family='Arial',font_size=19,fill='#fcdf9b'))
s.add(s.text('POWER = deep sleep/wake (not true supply OFF). STOP = authenticated remote shutdown request (not a safety emergency stop).',insert=(58,923),font_family='Arial',font_size=17,fill='#f7b6b6'))
s.save()
cairosvg.svg2png(url=str(ROOT/'schematics'/'wiring_overview.svg'),write_to=str(OUT/'wiring_overview.png'))
# editable 2D faceplate DXF with openings and mounting holes
import ezdxf
D=ezdxf.new('R2013');ms=D.modelspace()
D.layers.new('OUTLINE',dxfattribs={'color':7});D.layers.new('CUTOUTS',dxfattribs={'color':4});D.layers.new('MOUNTING',dxfattribs={'color':3})
ms.add_lwpolyline([(0,0),(142,0),(142,210),(0,210)],close=True,dxfattribs={'layer':'OUTLINE'})
for x,y,w,h in [(71,166,36,44),(71,118,66,17)]+[(x,y,12.6,12.6) for x,y in [(95,89),(120,89),(95,62),(120,62)]]:
 ms.add_lwpolyline([(x-w/2,y-h/2),(x+w/2,y-h/2),(x+w/2,y+h/2),(x-w/2,y+h/2)],close=True,dxfattribs={'layer':'CUTOUTS'})
ms.add_circle((39,79),9.1,dxfattribs={'layer':'CUTOUTS'})
for x in (8,134):
 for y in (8,202):ms.add_circle((x,y),1.65,dxfattribs={'layer':'MOUNTING'})
for x in (33.5,108.5):
 for y in (102.5,133.5):ms.add_circle((x,y),1.35,dxfattribs={'layer':'MOUNTING'})
D.saveas(ROOT/'cad'/'front_panel_layout.dxf')
print('Wrote preview images and wiring overview')
