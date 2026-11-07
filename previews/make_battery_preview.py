"""Draw an annotated layout of the actual parameterized battery-bay CAD."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from pathlib import Path
p=Path(__file__).with_name('battery_bay_layout.png')
fig=plt.figure(figsize=(14,8.5),facecolor='#101a24')
fig.text(0.055,.94,'COMPUTER DIRECTORY CONSOLE   /   REAR BATTERY COMPARTMENT',fontsize=20,color='white',weight='bold')
fig.text(0.055,.905,'v0.3  •  5 V regulated pack  •  removable 4-screw door  •  Fusion-compatible STEP + STL',fontsize=11,color='#a9c6d5')
ax1=fig.add_axes([.075,.18,.36,.67]);ax1.set_aspect('equal');ax1.set_xlim(-10,152);ax1.set_ylim(-6,222);ax1.axis('off')
ax1.add_patch(Rectangle((0,0),142,210,facecolor='#244552',edgecolor='#82bcd0',lw=2,joinstyle='round'))
ax1.add_patch(Rectangle((6,90),130,100,facecolor='#3d8c84',edgecolor='#8df1ce',lw=2))
ax1.add_patch(Rectangle((18,102),106,76,facecolor='#122a32',edgecolor='#bdedb7',lw=1.6,linestyle='--'))
for x in (12,130):
 for y in (96,184):
  ax1.add_patch(Circle((x,y),2.5,facecolor='#efd88c',edgecolor='#fff7d0',lw=0.8))
ax1.add_patch(Rectangle((98,160.5),18,11,facecolor='#f3d0ad',edgecolor='#fce6cc',lw=1))
ax1.text(71,147,'BATTERY CAVITY\n106 × 76 × 28 mm',color='#edfff7',ha='center',va='center',fontsize=11,weight='bold')
ax1.text(71,65,'Tray mounts on rear shell\nwith four M3 screws',color='#a6dfdc',ha='center',va='center',fontsize=10)
ax1.annotate('USB cable passage',xy=(107,166),xytext=(23,205),color='#f7ddb5',fontsize=9,arrowprops=dict(arrowstyle='->',color='#f7ddb5'))
ax1.text(71,-4,'142 mm',color='#d5eaf1',ha='center',va='top',fontsize=10)
ax1.text(-7,105,'210 mm',color='#d5eaf1',ha='center',va='center',rotation=90,fontsize=10)
ax1.set_title('A. REAR OF CONSOLE',color='white',fontsize=12,pad=12,fontweight='bold')
ax2=fig.add_axes([.55,.38,.37,.40]);ax2.set_aspect('equal');ax2.set_xlim(-8,140);ax2.set_ylim(-10,112);ax2.axis('off')
ax2.add_patch(Rectangle((0,0),130,100,facecolor='#367e81',edgecolor='#9eeadf',lw=2))
ax2.add_patch(Rectangle((12,12),106,76,facecolor='none',edgecolor='#c0eee6',linestyle='--',lw=1.3))
for x in (6,124):
 for y in (6,94):
  ax2.add_patch(Circle((x,y),1.5,facecolor='#0b2631',edgecolor='#f7d7a4',lw=1.1))
for x in (40,65,90):
 for y in (22,76):
  ax2.add_patch(Rectangle((x-9,y-1.5),18,3,facecolor='#142731',edgecolor='#bad6d3',lw=.3))
ax2.text(65,50,'VENTED\nBATTERY DOOR',color='white',ha='center',va='center',fontsize=11,fontweight='bold')
ax2.set_title('B. REMOVABLE BATTERY DOOR',color='white',fontsize=12,pad=14,fontweight='bold')
ax3=fig.add_axes([.51,.16,.43,.16]);ax3.set_xlim(0,100);ax3.set_ylim(0,30);ax3.axis('off')
ax3.add_patch(Rectangle((5,8),5,20,facecolor='#367e81',edgecolor='#a2e7e7'))
ax3.add_patch(Rectangle((10,8),31,20,facecolor='#244552',edgecolor='#a2e7e7'))
ax3.add_patch(Rectangle((41,8),29,20,facecolor='#397e70',edgecolor='#c4efdc'))
ax3.add_patch(Rectangle((70,8),3,20,facecolor='#e6c483',edgecolor='#fff4c0'))
ax3.text(7,3,'Front',color='#d3eef3',ha='center',fontsize=9)
ax3.text(25,3,'Rear case',color='#d3eef3',ha='center',fontsize=9)
ax3.text(56,3,'Battery tray',color='#d3eef3',ha='center',fontsize=9)
ax3.text(77,3,'Door',color='#e6d5b6',ha='center',fontsize=9)
ax3.set_title('C. ASSEMBLY DEPTH (SCHEMATIC)',color='white',fontsize=11,pad=5,fontweight='bold')
fig.text(.055,.06,'Suggested pack ≤100 × 70 × 23 mm  |  external bay adds 33.4 mm to depth  |  measure your actual regulated 5 V pack before printing',color='#a9c6d5',fontsize=10)
fig.savefig(p,dpi=160,facecolor=fig.get_facecolor());plt.close(fig)
print(p)
