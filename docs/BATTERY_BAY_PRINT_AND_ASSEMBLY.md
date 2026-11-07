# Rear 5 V Battery Bay (v0.3)

This revision keeps the existing front-panel layout and lettering, TFT window, 16×2 LCD window, joystick hole, buttons, and piezo grille **unchanged**. It adds a battery bay to the **outside of the REAR shell**, accessible through a removable screw-on hatch.

## Print THESE files for the revised enclosure

| File | Purpose | Qty |
| --- | --- | ---: |
| `stl/front_panel.stl` | Existing front panel, UNCHANGED | 1 |
| `stl/rear_shell_with_battery_mount.stl` | Modified rear case with power-cable hole and 4 mounting holes | 1 |
| `stl/battery_tray_5V.stl` | External enclosed battery compartment, mounted to back | 1 |
| `stl/battery_door_5V.stl` | Removable ventilated hatch with alignment tongue | 1 |
| `stl/square_button_trim.stl` | Existing optional button trim | 4 |

**Do not print `stl/rear_shell.stl`** for the battery-backed build. That is the older version without tray mounting holes. The `rear_shell_original.step` file is preserved as source for the revised CAD generator.

## Dimensions (nominal, millimetres)

- Main enclosure footprint: **142 x 210 mm**, unchanged.
- External battery tray outer footprint: **130 x 100 mm**.
- Battery cavity: **106 x 76 x 28 mm** before hatch alignment lip.
- **Suggested maximum actual pack size: 100 x 70 x 23 mm** (allow wiring/foam clearance; measure the pack first).
- Battery door plate thickness: **2.4 mm**; alignment lip height **2.2 mm**; clearance **0.7 mm per side**.
- Tray external depth: **31 mm**; cover adds **2.4 mm**.
- Overall enclosure assembled depth with decorative button trims: approximately **72.2 mm** (z=-33.4 to z=38.8).
- Interior-to-bay cable slot: **18 x 11 mm**, centered at x=107, y=166. Test that your particular USB connector head fits before printing.

The battery bay is a generic size, **not a fit-guarantee** for an unspecified 5 V battery. It is intended for a compact, finished, protected, regulated 5 V **USB battery/power bank** that physically fits within these dimensions. It is not designed for exposed individual cells.

## Fasteners

- **4 x M3 x 10 mm screws**, driven FROM INSIDE the main console through holes in its back plate into blind pilot holes in the tray (pilot diameter 2.55 mm). If your plastic or screws differ, test a pilot first, or use properly sized inserts.
- **4 x M2.5 x 8 mm screws**, driven from the OUTSIDE through the battery door into the four tray blind pilot holes (pilot diameter 2.05 mm).
- A thin foam strip or hook-and-loop pad for battery retention (recommended); optional insulating tape.

The two sets of blind pilot holes are on opposite ends of the tray. The upper mount holes and the outer-door pilot holes do **not** run through each other. Do not overtighten and crack the printed plastic.

## Recommended slicer settings

PLA or PETG, 0.20 mm layers, 3–4 walls, 20–30% infill. For the first test print, use approximately 0.2 mm dimensional compensation if your printer tends to fuse fitted parts. Support need is low when each part is oriented correctly:

1. **Main rear shell:** print its broad outer back face touching the build plate, with the original enclosure opening facing upward (same as the old rear shell).
2. **Battery tray:** rotate so the large **solid floor** (the face that touches the main case) is ON the build plate; battery opening faces upward. Do not print with opening against the bed.
3. **Battery door:** print with its flat OUTER face on the build plate; small location tongue faces upward.
4. **Front:** keep your previous successful front-panel orientation/settings. The embossed or engraved lettering may benefit from 0.16 mm layers.

If print supports are generated under the small hatch thumb notch, inspect the orientation and disable unnecessary support. After printing, deburr screws and lightly sand hatch lip only if necessary.

## Mechanical assembly (before wiring)

1. Place rear shell on a flat surface with **outside back face upward**.
2. Align the external tray so its **solid floor** touches the outer rear shell and the 4 corner pilot holes align with the rear-shell clearance holes. The two **18 x 11 mm cable slots** must align.
3. From inside the rear shell, insert four M3 x 10 mm screws into the tray's upper pilot holes. Tighten gently.
4. Feed your USB cable or protected 5 V output lead through the aligned slot, leaving slack and avoiding pressure against the case edge. Add a grommet or edge protection for the cable.
5. Place the actual regulated 5 V battery pack in the cavity, secured with removable hook-and-loop/foam so it cannot hit the lid. Verify no metal is exposed or able to short.
6. Place the battery door with its printed alignment tongue inside the opening; check the 0.7 mm radial clearance.
7. Install four M2.5 x 8 mm screws into the tray's outer pilot holes. The hatch is removable for battery servicing.
8. Before installing electronics or connecting a battery, do a dry run and verify the main case still closes and that the USB connector/power lead fits.

The battery door has six ventilation slots. Do not block them with a battery pouch. The bay is NOT weatherproof, fireproof or suitable for an unprotected bare lithium cell.

## Electrical notes (IMPORTANT)

- A **regulated 5.0 V** power-bank output is NOT the same as a bare single 3.7 V lithium-ion cell or two AA cells.
- For a standard ESP32 DevKit, a compliant regulated 5 V USB source can usually power the board through its **USB input**; confirm your board and avoid simultaneous uncontrolled power-path connections.
- The display modules, backlight, SD adapter and LCD must still be wired at their **correct voltage/logic levels**. This case change does not modify or solve the screen power requirements.
- A power bank may automatically turn off when current draw drops in ESP32 deep sleep. If it does, pressing the RED button may no longer wake the board. Test this behavior and use an appropriate actual power-latch or battery-management design if physical on/off is required.
- **Never** connect an unknown '5 V battery' to the ESP32's 3V3 pin. No bare battery leads should touch the printed enclosure or circuit contacts.
- Avoid charging, placing a damaged pack inside, or operating a hot pack in a closed PLA container. Follow the pack maker's operating and charging instructions.

## Fusion 360 editing

- Complete revised assembly: `cad/Console_Assembly_with_5V_Battery.step`.
- Separate parts: `cad/rear_shell_with_battery_mount.step`, `cad/battery_tray_5V.step`, `cad/battery_door_5V.step`.
- Parametric construction script: `cad/make_modular_5V_battery_bay.py`, which uses `cad/rear_shell_original.step` as input. Install Python/CadQuery to regenerate.
- This is an editable **STEP assembly**, not a native Autodesk `.f3d` file; real-world fit must be checked. The original Fusion/EAGLE circuit schematic and software project are unchanged.

## First-fit checklist

- [ ] Actual 5 V battery pack fits ≤100 x 70 x 23 mm with cable bend clearance.
- [ ] Rear tray bottom sits flat against original back with all 4 holes aligned.
- [ ] M3 screws seat without splitting plastic; screw tips do not enter the pack cavity.
- [ ] Battery door lip inserts freely, door can be removed, and all M2.5 screws engage.
- [ ] No metal rubs against the battery or the cable hole.
- [ ] ESP32 boots from regulated 5 V source; check operating and deep-sleep behavior.
- [ ] Display and BLE performance are unchanged after enclosed assembly.
