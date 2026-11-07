"""Rear battery compartment: print-friendly modular version.

Modifies original v0.2 case only to add four mount holes and an 18x11mm
cable-entry hole. Prints the 5V pack tray separately, fixing it from the
INSIDE of the case with four M3 screws (pilot holes in the tray). The hatch
uses four M2.5 screws (separate blind pilot holes on the external side).

Requires CadQuery. Open Fusion with supplied STEP models. Millimetres.
"""
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
CAD, STLS = ROOT/'cad', ROOT/'stl'

CENTER_X, CENTER_Y = 71.0, 140.0
OUT_W, OUT_H = 130.0, 100.0
IN_W, IN_H = 106.0, 76.0
TRAY_LO, TRAY_HI = -31.0, 0.0
FLOOR_Z = -3.0
DOOR_TH = 2.4
LIP_Z = 2.2
CLEARANCE = 0.7
LIP_THICKNESS = 1.5
SCREW_XY = [(12.0,96.0),(130.0,96.0),(12.0,184.0),(130.0,184.0)]
M3_CASE_CLEARANCE = 3.4
M3_TRAY_PILOT = 2.55
M25_DOOR_CLEARANCE = 2.9
M25_TRAY_PILOT = 2.05

original = cq.importers.importStep(str(CAD/'rear_shell_original.step'))
case = original
# A single 18x11mm cable slot through the 2.7mm back panel (part z=0..34).
cable_slot = (cq.Workplane('XY')
    .box(18,11,4.5,centered=(True,True,False)).translate((107,166,-0.5)))
case = case.cut(cable_slot)

# Four holes in the original back plate. Screws inserted from the OPEN/front
# side of the console after hardware assembly, into the bay's upper pilots.
for x,y in SCREW_XY:
    drill = cq.Workplane('XY').center(x,y).circle(M3_CASE_CLEARANCE/2).extrude(4).translate((0,0,-0.5))
    case = case.cut(drill)

# Solid external tray blank. z=0 mounts to original case's outside rear face.
tray = (cq.Workplane('XY')
        .box(OUT_W,OUT_H,TRAY_HI-TRAY_LO,centered=(True,True,False))
        .translate((CENTER_X,CENTER_Y,TRAY_LO)))
# Open from rear (negative z), with 3mm solid floor adjacent to case.
pocket = (cq.Workplane('XY')
        .box(IN_W,IN_H,FLOOR_Z-TRAY_LO+0.2,centered=(True,True,False))
        .translate((CENTER_X,CENTER_Y,TRAY_LO-0.2)))
tray = tray.cut(pocket)
# Cable hole joins battery bay to the interior of the main enclosure.
tray = tray.cut((cq.Workplane('XY')
    .box(18,11,3.8,centered=(True,True,False)).translate((107,166,FLOOR_Z-0.4))))
# Upper mounting pilots from the front at z=0 toward z=-10.5.
# They are blind and are isolated from the hatch holes by a solid section.
for x,y in SCREW_XY:
    p = (cq.Workplane('XY').center(x,y).circle(M3_TRAY_PILOT/2)
         .extrude(10.5).translate((0,0,-10.5)))
    tray = tray.cut(p)
    p2 = (cq.Workplane('XY').center(x,y).circle(M25_TRAY_PILOT/2)
          .extrude(10.0).translate((0,0,TRAY_LO-0.05)))
    tray = tray.cut(p2)

# Door fits flush against the bay rear rim at z=-31.0; exterior at z=-33.4.
door = (cq.Workplane('XY')
        .box(OUT_W,OUT_H,DOOR_TH,centered=(True,True,False))
        .translate((CENTER_X,CENTER_Y,TRAY_LO-DOOR_TH)))
# Alignment lip extends into cavity with radial 0.7mm clearance.
lip_outer = (cq.Workplane('XY')
        .box(IN_W-2*CLEARANCE,IN_H-2*CLEARANCE,LIP_Z,centered=(True,True,False))
        .translate((CENTER_X,CENTER_Y,TRAY_LO)))
lip_inner = (cq.Workplane('XY')
        .box(IN_W-2*CLEARANCE-2*LIP_THICKNESS,
             IN_H-2*CLEARANCE-2*LIP_THICKNESS,LIP_Z+0.4,centered=(True,True,False))
        .translate((CENTER_X,CENTER_Y,TRAY_LO-0.2)))
door = door.union(lip_outer.cut(lip_inner))
for x,y in SCREW_XY:
    screw_hole = (cq.Workplane('XY').center(x,y)
        .circle(M25_DOOR_CLEARANCE/2).extrude(DOOR_TH+0.4)
        .translate((0,0,TRAY_LO-DOOR_TH-0.2)))
    door = door.cut(screw_hole)
# Finger notch nibble along near y edge, away from fastener locations.
notch = (cq.Workplane('XY').center(CENTER_X,CENTER_Y-OUT_H/2-2.2)
         .circle(6).extrude(DOOR_TH+0.4)
         .translate((0,0,TRAY_LO-DOOR_TH-0.2)))
door = door.cut(notch)
# Air slots provide modest passive ventilation around a regulated USB power pack.
# Do not charge an unknown/damaged lithium pack unattended inside a printed box.
for x in (46, 71, 96):
    for y in (112, 166):
        vent = (cq.Workplane('XY')
            .box(18.0, 3.0, DOOR_TH + 0.6, centered=(True,True,False))
            .translate((x, y, TRAY_LO-DOOR_TH-0.3)))
        door = door.cut(vent)

items = [
    (case,'rear_shell_with_battery_mount'),
    (tray,'battery_tray_5V'),
    (door,'battery_door_5V')
]
for part,name in items:
    cq.exporters.export(part,str(CAD/(name+'.step')))
    cq.exporters.export(part,str(STLS/(name+'.stl')),tolerance=0.04,angularTolerance=0.14)

front = cq.importers.importStep(str(CAD/'front_panel.step'))
trim = cq.importers.importStep(str(CAD/'square_button_trim.step'))
a = cq.Assembly(name='Computer_Directory_Console_battery_modular')
a.add(case,name='Updated_main_rear_shell',color=cq.Color(.1,.28,.32))
a.add(tray,name='5V_pack_tray',color=cq.Color(.16,.4,.42))
a.add(door,name='Removable_battery_door',color=cq.Color(.14,.42,.48))
a.add(front,name='Front_panel',loc=cq.Location(cq.Vector(0,0,34)),color=cq.Color(.16,.45,.45))
for i,(x,y) in enumerate([(95,89),(120,89),(95,62),(120,62)],1):
    a.add(trim,name='Square_button_trim_'+str(i),loc=cq.Location(cq.Vector(x,y,37)))
a.save(str(CAD/'Console_Assembly_with_5V_Battery.step'))
print('Exported 3 STL, 3 STEP, and updated STEP assembly.')
