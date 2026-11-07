"""Generate original placeholder vector portraits and BMPs for ST7789."""
from pathlib import Path
from io import BytesIO
import cairosvg
from PIL import Image
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'avatars'; OUT.mkdir(exist_ok=True)
profiles=[
 ('heather','Heather','#c74b88','#171923','#7c3a63','#f1c2a0','long'),
 ('lindsay','Lindsay','#f5c44a','#f7d15e','#81b9e9','#f5cfb5','waves'),
 ('zoey','Zoey','#d97450','#bd482e','#6ab58b','#efd1b6','side'),
 ('gwen','Gwen','#6972b7','#222834','#3196a6','#e8c9bd','fringe'),
 ('courtney','Courtney','#ba6d4c','#623b30','#8b7fa9','#c99279','bob'),
]
for slug,name,bg,hair,shirt,skin,style in profiles:
 hair_back = {
  'long':'<path d="M47 75 Q20 59 36 31 Q48 7 80 14 Q108 18 114 53 L114 120 L43 120Z" fill="HAIR"/>',
  'waves':'<path d="M42 71 Q18 47 31 24 Q48 -1 81 13 Q115 11 119 52 Q135 79 119 119 L36 119 Q22 96 42 71" fill="HAIR"/>',
  'side':'<path d="M44 67 Q22 41 41 21 Q62 0 92 17 Q111 33 113 60 L111 116 L45 116Z" fill="HAIR"/>',
  'fringe':'<path d="M35 60 Q30 11 75 13 Q119 14 118 66 L117 123 L34 123Z" fill="HAIR"/>',
  'bob':'<path d="M39 46 Q29 9 78 12 Q118 10 118 53 L122 91 Q100 110 78 96 Q49 111 32 89Z" fill="HAIR"/>',
 }[style].replace('HAIR',hair)
 hair_front = {
  'long':'<path d="M43 60 Q37 36 48 26 Q75 40 100 24 Q111 38 106 55 Q98 34 91 40 Q69 44 48 37Z" fill="HAIR"/>',
  'waves':'<path d="M42 56 Q33 27 64 22 Q88 9 110 34 Q98 32 95 39 Q65 39 46 32Z" fill="HAIR"/>',
  'side':'<path d="M41 52 Q38 25 72 19 Q94 15 108 38 Q85 31 58 44 Q45 43 43 60Z" fill="HAIR"/>',
  'fringe':'<path d="M42 54 Q33 21 75 17 Q106 15 110 52 Q96 43 89 29 Q82 51 56 43 Q48 48 42 54Z" fill="HAIR"/>',
  'bob':'<path d="M43 56 Q34 27 62 21 Q96 12 111 41 Q92 39 74 28 Q60 44 42 44Z" fill="HAIR"/>',
 }[style].replace('HAIR',hair)
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 160 160">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="#24263f"/></linearGradient></defs>
<rect width="160" height="160" rx="15" fill="url(#g)"/>
<circle cx="131" cy="32" r="30" fill="#fff" opacity=".11"/>
<path d="M7 150 Q17 112 53 108 L107 108 Q143 112 152 150Z" fill="{shirt}"/>
{hair_back}
<path d="M63 98 L63 113 Q80 130 97 113 L97 98Z" fill="{skin}"/>
<ellipse cx="80" cy="65" rx="35" ry="45" fill="{skin}"/>
{hair_front}
<path d="M55 65 Q64 60 71 66 M89 66 Q97 60 106 65" fill="none" stroke="#3e3034" stroke-width="2.2" stroke-linecap="round"/>
<circle cx="64" cy="67" r="2.4" fill="#252735"/><circle cx="97" cy="67" r="2.4" fill="#252735"/>
<path d="M75 82 Q81 85 86 82" fill="none" stroke="#a8756f" stroke-width="1.8"/>
<path d="M67 93 Q80 100 93 93" fill="none" stroke="#9a4b5b" stroke-width="2.5" stroke-linecap="round"/>
<rect x="7" y="130" rx="6" width="146" height="25" fill="#101929" opacity=".84"/>
<text x="80" y="148" font-family="DejaVu Sans,Arial" font-size="15" font-weight="bold" fill="white" text-anchor="middle">{name}</text>
</svg>'''
 (OUT/(slug+'.svg')).write_text(svg,encoding='utf-8')
 png=cairosvg.svg2png(bytestring=svg.encode(),output_width=300,output_height=300)
 (OUT/(slug+'.png')).write_bytes(png)
 # 120x120 24-bit BMP, supported by firmware BMP decoder
 img=Image.open(BytesIO(png)).convert('RGB').resize((120,120),Image.Resampling.LANCZOS)
 img.save(OUT/(slug+'.bmp'),format='BMP')
print('Generated',len(profiles),'custom placeholder avatars')
