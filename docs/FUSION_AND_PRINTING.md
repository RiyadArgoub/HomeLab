> **v0.3 battery revision:** This page originally described the v0.2 shell. For the current battery-backed build, use `stl/rear_shell_with_battery_mount.stl`, `stl/battery_tray_5V.stl`, and `stl/battery_door_5V.stl` along with the unchanged front and trims. See [BATTERY_BAY_PRINT_AND_ASSEMBLY.md](BATTERY_BAY_PRINT_AND_ASSEMBLY.md). Import `cad/Console_Assembly_with_5V_Battery.step` for the updated Fusion assembly.

# Autodesk Fusion and 3D Printing Guide

## Deliverable files

- `cad/Console_Assembly.step`: **multi-part STEP assembly** with rear shell, front panel and four button-trim instances, correctly positioned. Import into Fusion as a 3D model and save to a Fusion native design if desired.
- `cad/front_panel.step`, `cad/rear_shell.step`, `cad/square_button_trim.step`: independent STEP solids, editable with Fusion's imported-body tools.
- `stl/front_panel.stl`, `stl/rear_shell.stl`, `stl/square_button_trim.stl`: watertight printable meshes. Print trim **4 copies** or omit it if your panel-mount buttons already have attractive square caps.
- `cad/generate_enclosure.py`: fully editable CadQuery generator (mm). Change `W`, `H`, `DEPTH`, openings and text, then rerun to regenerate STL/STEP.
- `cad/front_panel_layout.dxf`: 2D front cutout reference for Fusion sketches; **not** a CNC-ready manufacturing drawing.
- `schematics/Directory_Interconnect.sch`: generated EAGLE XML **module-level wiring schematic** intended for Fusion Electronics import. It uses **generic connector packages**, not physical PCB footprints. No custom PCB or routed `.brd` has been designed. Fusion compatibility has not been tested in a live Fusion installation.
- `schematics/wiring_overview.svg` and `previews/wiring_overview.png`: human-readable electrical pin mapping.

## Nominal enclosure dimensions

| Dimension/feature | First-pass CAD (mm) |
| --- | ---: |
| Front face | 142 wide × 210 high |
| Rear shell | 34 deep |
| Front panel | 3 thick |
| Total case (without trim) | ~37 deep |
| ST7789 visual window | 36 × 44 |
| 16×2 LCD visual window | 66 × 17 |
| Joystick shaft opening | Ø18.2 |
| Square button apertures | 12.6 × 12.6 each |
| Screw clearance in front panel | Ø3.3, 4× (M3) |
| Pilot holes in rear posts | Ø2.6, 4× (check screw type / tap) |
| 16×2 LCD mounting holes | Nominal 75 × 31 pattern, Ø2.7 |
| Optional TFT securing slots | 2.3 × 5, four around window |
| Piezo grille perforations | Ø1.8 |
| USB cable service notch | Nominal 13×11 opening in lower rear wall |
| microSD side access | Nominal access cutout, exact module position TBD |

**These are not final-fit dimensions.** No measurements were provided for your specific 2-inch TFT PCB, LCD mounting hole pattern, joystick board, panel switches, ESP32 DevKit, microSD breakout or piezo diameter. Their different vendor dimensions can cause collisions. The TFT retaining slots and internal anchor posts are generic and may need adhesive pads, printed brackets, cable ties or revision for real boards.

## 3D print suggestions (QIDI or other printer)

1. Import all three STLs into your slicer individually. Do **not** print the preassembled STEP as one fused object.
2. Place the front plate flat with the **unlettered rear surface** on the bed and the engraved neutral front-panel title facing upward. The small-letter engraving benefits from a 0.16–0.20 mm layer height.
3. Place the rear shell with its solid back surface on the bed and walls pointing upward.
4. Place the optional trims flat on the bed; print four and optionally assign red/yellow/green/blue material colors.
5. Start with **PLA or PETG, 0.2 mm layer height, 3 perimeters, 15–20% infill**, and evaluate thin walls and overhangs in slicer preview. Supports should not be needed for most geometry, but the side-access notches may need tuning.
6. Dry-fit the displays, joystick, buttons, ESP32 and SD module BEFORE wiring or fastening. Check for exposed leads shorting against another module.
7. Use **4× M3** case screws only after checking pilot-hole engagement and clearance, plus the appropriate separate board fasteners or mounting tape/ties. Do not overtighten printed posts.
8. Confirm antenna-free region and metal-free space around RFID? This console has **no RFID reader**: the earlier RFID enclosure is a different project.

## Fusion workflow

Open Fusion, upload `.step` assembly or import individual `.step` parts, then save as a native Fusion document. For Electronics, use a new Electronics Design and import `.sch`. Validate that all net labels, pins and devices were imported before relying on it. Autodesk's formats support STEP, STL, DXF and EAGLE `.sch`, but our custom file has not been opened in Fusion here.

The assembly STEP is a mechanical starting point, not a complete component-level CAD assembly. The `.sch` does not constitute a PCB design, so manufacturing files, trace widths, footprints and electrical clearance validation are **future work**.

## Expected battery behavior

The present model is **USB-powered** and has no AA battery holder. This is intentional: your dual-display ESP32 build requires more stable power than connecting 2×AA cells directly to the ESP32 can provide. A future battery revision would need a verified regulator, switching arrangement and measured runtime. For true OFF/ON from the RED momentary square button, add a designed latching power-switch module; currently the red button uses ESP32 deep sleep and RTC wake only.
