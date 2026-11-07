"""Generate EAGLE XML module-level schematic for Autodesk Fusion Electronics.
Schematic is logical interconnect document, NOT a fabrication-ready PCB layout.
Use precise net labels as the source of truth and verify against real boards.
"""
from pathlib import Path
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'schematics'
MODULES={
 'U1':('ESP32_DEVKIT',['3V3','GND','GPIO23','GPIO18','GPIO19','GPIO16','GPIO17','GPIO14','GPIO13','GPIO21','GPIO22','GPIO34','GPIO35','GPIO32','GPIO33','GPIO25','GPIO26','GPIO27'],(15,264)),
 'DS1':('ST7789V',['VCC','GND','DIN','CLK','CS','DC','RST','BL'],(115,264)),
 'J1':('MICROSD_SPI',['VCC','GND','MOSI','SCK','MISO','CS'],(115,196)),
 'DS2':('LCD1602_I2C',['VCC','GND','SDA','SCL'],(115,135)),
 'J2':('JOYSTICK',['VCC','GND','VRX','VRY'],(115,96)),
 'SW1':('BUTTON_POWER',['GPIO','GND'],(198,259)),
 'SW2':('BUTTON_BACK',['GPIO','GND'],(198,227)),
 'SW3':('BUTTON_PRESS',['GPIO','GND'],(198,195)),
 'SW4':('BUTTON_STOP',['GPIO','GND'],(198,163)),
 'BZ1':('PIEZO',['PLUS','MINUS'],(198,125)),
}
# One label per signal / EAGLE net, attached to ESP32 and appropriate module pins.
NETS={
 'P3V3':[('U1','3V3'),('DS1','VCC'),('J1','VCC'),('DS2','VCC'),('J2','VCC')],
 'GND':[('U1','GND'),('DS1','GND'),('J1','GND'),('DS2','GND'),('J2','GND'),('SW1','GND'),('SW2','GND'),('SW3','GND'),('SW4','GND'),('BZ1','MINUS')],
 'SPI_MOSI_GPIO23':[('U1','GPIO23'),('DS1','DIN'),('J1','MOSI')],
 'SPI_SCK_GPIO18':[('U1','GPIO18'),('DS1','CLK'),('J1','SCK')],
 'SPI_MISO_GPIO19':[('U1','GPIO19'),('J1','MISO')],
 'TFT_CS_GPIO16':[('U1','GPIO16'),('DS1','CS')],
 'TFT_DC_GPIO17':[('U1','GPIO17'),('DS1','DC')],
 'TFT_RST_GPIO14':[('U1','GPIO14'),('DS1','RST')],
 'SD_CS_GPIO13':[('U1','GPIO13'),('J1','CS')],
 'I2C_SDA_GPIO21':[('U1','GPIO21'),('DS2','SDA')],
 'I2C_SCL_GPIO22':[('U1','GPIO22'),('DS2','SCL')],
 'JOY_X_GPIO34':[('U1','GPIO34'),('J2','VRX')],
 'JOY_Y_GPIO35':[('U1','GPIO35'),('J2','VRY')],
 'POWER_GPIO32':[('U1','GPIO32'),('SW1','GPIO')],
 'BACK_GPIO33':[('U1','GPIO33'),('SW2','GPIO')],
 'PRESS_GPIO25':[('U1','GPIO25'),('SW3','GPIO')],
 'STOP_GPIO26':[('U1','GPIO26'),('SW4','GPIO')],
 'PIEZO_GPIO27':[('U1','GPIO27'),('BZ1','PLUS')],
}

def sub(parent,tag,**kwargs):return ET.SubElement(parent,tag,{k:str(v) for k,v in kwargs.items()})
eagle=ET.Element('eagle',{'version':'9.6.2'})
draw=sub(eagle,'drawing');settings=sub(draw,'settings');sub(settings,'setting',alwaysvectorfont='no',verticaltext='up')
sub(draw,'grid',distance='2.54',unitdist='mm',unit='mm',style='lines',multiple='1',display='no')
layers=sub(draw,'layers')
for num,name,color in [(91,'Nets',2),(92,'Busses',1),(93,'Pins',2),(94,'Symbols',4),(95,'Names',7),(96,'Values',7),(97,'Info',7)]:
 sub(layers,'layer',number=num,name=name,color=color,fill='1',visible='yes',active='yes')
schematic=sub(draw,'schematic',xreflabel='%F%N/%S.%C',xrefpart='/%S.%C')
libraries=sub(schematic,'libraries');lib=sub(libraries,'library',name='PROTOTYPE_MODULES')
packages=sub(lib,'packages');symbols=sub(lib,'symbols');deviceSets=sub(lib,'devicesets')
types={v[0]:v[1] for k,v in MODULES.items()}
for typ,pins in types.items():
 pkg=sub(packages,'package',name='GENERIC_'+typ)
 for n,p in enumerate(pins):
  sub(pkg,'pad',name=str(n+1),x=2.54*n,y=0,drill='0.8',diameter='1.8')
 symbol=sub(symbols,'symbol',name=typ)
 height=max(15.24,(len(pins)-1)*5.08+7.62)
 sub(symbol,'wire',x1='-5.08',y1=str(-height+5.08),x2='22.86',y2='5.08',width='0.254',layer='94')
 sub(symbol,'text',x='-2.54',y='1.27',size='2.54',layer='95').text='>'+ 'NAME'
 for n,p in enumerate(pins):
  sub(symbol,'pin',name=p,x='25.4',y=str(-n*5.08),visible='pin',length='short',direction='pas',rot='R180')
 ds=sub(deviceSets,'deviceset',name=typ,prefix={'ESP32_DEVKIT':'U','ST7789V':'DS','LCD1602_I2C':'DS','MICROSD_SPI':'J','JOYSTICK':'J','PIEZO':'BZ'}.get(typ,'SW'),uservalue='yes')
 gates=sub(ds,'gates');sub(gates,'gate',name='G$1',symbol=typ,x=0,y=0,addlevel='always')
 devices=sub(ds,'devices');dev=sub(devices,'device',name='',package='GENERIC_'+typ)
 connects=sub(dev,'connects')
 for n,p in enumerate(pins):sub(connects,'connect',gate='G$1',pin=p,pad=str(n+1))
 sub(dev,'technologies').append(ET.Element('technology',{'name':''}))
sub(schematic,'attributes');sub(schematic,'variantdefs')
classes=sub(schematic,'classes');sub(classes,'class',number=0,name='default',width=0,drill=0)
parts=sub(schematic,'parts')
for instance,(typ,pins,pos) in MODULES.items():sub(parts,'part',name=instance,library='PROTOTYPE_MODULES',deviceset=typ,device='')
sheets=sub(schematic,'sheets');sheet=sub(sheets,'sheet');plain=sub(sheet,'plain')
sub(plain,'text',x='12.7',y='287',size='4.0',layer='97').text='ESP32 COMPUTER DIRECTORY CONSOLE'
for i,line in enumerate([
 'MODULE-LEVEL WIRING SCHEMATIC -- NOT A PCB FABRICATION DESIGN',
 'IMPORTANT: LCD 1602 I2C only attach directly to 3.3V if module supports 3.3V.',
 'If I2C LCD board requires 5V, insert bidirectional level shifter on SDA/SCL.',
 'ST7789 BL pin is NOT shown as powered: verify module backlight requirements.',
 'All GPIO logic is 3.3V. Separate suitable 5V USB power powers ESP32 DevKit.',
 'Red POWER button triggers DEEP SLEEP; it does not physically cut the supply.'
]):
 sub(plain,'text',x='12.7',y=str(280-i*4.6),size='1.8',layer='97').text=line
instances=sub(sheet,'instances')
for name,(typ,pins,(x,y)) in MODULES.items():sub(instances,'instance',part=name,gate='G$1',x=x,y=y,rot='R0',smashed='no')
sub(sheet,'busses')
nets=sub(sheet,'nets')
for netname,members in NETS.items():
 net=sub(nets,'net',name=netname,**{'class':'0'})
 for name,pin in members:
  typ,pins,(ox,oy)=MODULES[name]
  y=oy-pins.index(pin)*5.08; x=ox+25.4
  seg=sub(net,'segment');sub(seg,'pinref',part=name,gate='G$1',pin=pin)
  sub(seg,'wire',x1=str(x),y1=str(y),x2=str(x+10.16),y2=str(y),width='0.1524',layer=91)
  sub(seg,'label',x=str(x+7.62),y=str(y),size='1.27',layer=95,rot='R0')
# BL is deliberately unconnected. Mark as NC until verified.
xml=minidom.parseString(ET.tostring(eagle,encoding='utf-8')).toprettyxml(indent='  ',encoding='utf-8')
(OUT/'Directory_Interconnect.sch').write_bytes(b'<!DOCTYPE eagle SYSTEM "eagle.dtd">\n'+xml[xml.find(b'<eagle'):])
import csv
with (OUT/'pin_map.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['net','modules_and_pins'])
 for name,members in NETS.items():writer.writerow([name,'; '.join('%s.%s'%p for p in members)])
print('Wrote',OUT/'Directory_Interconnect.sch')
