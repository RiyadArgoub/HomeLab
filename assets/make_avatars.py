"""Generate the neutral non-human placeholder avatar used by the demo registry."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'avatars'; OUT.mkdir(exist_ok=True)
def build(size):
    im=Image.new('RGB',(size,size),(236,239,242)); d=ImageDraw.Draw(im); s=size/240
    d.rounded_rectangle((18*s,18*s,222*s,222*s),radius=24*s,fill=(221,226,231),outline=(99,112,124),width=max(1,int(4*s)))
    d.rounded_rectangle((50*s,58*s,190*s,150*s),radius=10*s,fill=(246,248,250),outline=(55,67,78),width=max(1,int(6*s)))
    d.rectangle((112*s,150*s,128*s,178*s),fill=(55,67,78)); d.rounded_rectangle((86*s,175*s,154*s,187*s),radius=5*s,fill=(55,67,78))
    d.line((78*s,94*s,94*s,108*s),fill=(76,92,106),width=max(1,int(5*s))); d.line((94*s,108*s,78*s,122*s),fill=(76,92,106),width=max(1,int(5*s))); d.line((106*s,122*s,145*s,122*s),fill=(76,92,106),width=max(1,int(5*s)))
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',max(9,int(24*s)))
    except Exception: font=None
    box=d.textbbox((0,0),'PC',font=font); d.text(((size-(box[2]-box[0]))/2,196*s),'PC',font=font,fill=(55,67,78))
    return im
build(240).save(OUT/'placeholder.png','PNG')
build(120).save(OUT/'placeholder.bmp','BMP')
(OUT/'placeholder.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240"><rect x="18" y="18" width="204" height="204" rx="24" fill="#dde2e7" stroke="#63707c" stroke-width="4"/><rect x="50" y="58" width="140" height="92" rx="10" fill="#f6f8fa" stroke="#37434e" stroke-width="6"/><rect x="112" y="150" width="16" height="28" fill="#37434e"/><rect x="86" y="175" width="68" height="12" rx="5" fill="#37434e"/><path d="M78 94 L94 108 L78 122 M106 122 H145" fill="none" stroke="#4c5c6a" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><text x="120" y="220" text-anchor="middle" font-family="DejaVu Sans,Arial" font-size="24" font-weight="bold" fill="#37434e">PC</text></svg>',encoding='utf-8')
print('Generated neutral placeholder avatar')
