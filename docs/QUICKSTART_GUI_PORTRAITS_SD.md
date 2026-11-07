# Console v0.5: Images, Names, GUI and 1 GB microSD

## Current image workflow

The public project bundles only one generic non-human placeholder image under
`assets/avatars/`. Custom device images never transfer through Bluetooth. The ESP32
needs a physical microSD card with the referenced BMP files in its root directory.

## 1. Run the GUI

Windows PowerShell (from the folder that contains this README):

```powershell
py -m pip install -r python_gui/requirements.txt
py python_gui/console_manager.py
```

Arch Linux (Python venv, requires tkinter system package, e.g. `tk`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r python_gui/requirements.txt
python python_gui/console_manager.py
```

Click on a computer in the left list. On the right, change Name, Role, Host,
Notes, etc. Click **Save changes**. This writes `assets/computers.json` on the PC.
`host` entries in the package are DEMO examples, not verified devices.

**Choose / replace image** accepts a PNG, JPG, WEBP, GIF or BMP. It makes:

- `assets/avatars/<name>.png`: PC GUI thumbnail.
- `assets/avatars/<name>.bmp`: ESP32 120x120 RGB 24-bit uncompressed BMP.

The image is **center-cropped to a square**, not stretched. The old `.svg`
original artwork is not updated by custom photo imports.

The **avatar** field should contain a simple `.bmp` filename, e.g. `placeholder.bmp` or `pc01.bmp`. The v0.5 firmware accepts filenames up to 31 characters before `.bmp`; use letters, digits, underscores, and hyphens for portability.

## 2. Prepare the 1 GB microSD

1. Back up anything important on the card. Format with an MBR partition and
   FAT16 or FAT32 (whichever your card formatter supports). Do not use exFAT.
2. In the GUI click **Export microSD files**. Choose an empty staging folder,
   e.g. `Desktop\Console_SD`. The tool creates `computers.csv` and the named
   BMP images using the **latest saved GUI records**.
3. Copy the generated files directly to the **ROOT** of the microSD card, not
   inside an `assets`, `avatars`, `sd_card`, or `Console_SD` subfolder.
4. Safely eject, insert into the 3.3V-compatible microSD reader, then reboot
   the ESP32. Open Arduino Serial Monitor at **115200 baud** for diagnostic
   output such as `SD init failed`.

Expected card layout:

```
/ (root)
  computers.csv
  placeholder.bmp
```

The supplied generic placeholder is small, so a 1 GB card has ample space. **1 GB is far more than sufficient.** The ESP32 program supports
up to **128 registry entries**, while the current screen draws a scrolling 9-row
window. The SD card is not a log drive; status updates are held in RAM and records
are saved on BLE sync events. **Avoid removing the card during a write.**

Optional command-line method:

```bash
python tools/prepare_sd.py --output sd_card
```

The project already contains a prebuilt `sd_card` folder for first boot.

### IMPORTANT: Bluetooth updates text but NOT image files

- GUI **Push selection** or **Push all to ESP32** updates records over BLE;
  firmware saves text to `/computers.csv` on the card.
- Changing a custom picture ALWAYS needs the new `.bmp` copied physically to
  microSD. Do not expect Push all to send image bytes.
- If editing on card directly, use `|`-separated text fields, not a normal
  comma-separated spreadsheet export:
  `name|role|host|mac|avatar|UNKNOWN|notes`.

## 3. GUI buttons

| GUI control | What it does |
|---|---|
| Select row | Open computer information, avatar and form |
| Save changes | Save edited entries to `assets/computers.json` |
| Choose / replace image | Convert/import image into GUI+ESP32 formats |
| Export microSD files | Generate root `computers.csv` and `.bmp` files |
| Connect Bluetooth | Find `DirectoryConsole` and connect over BLE |
| Push selection | Send current record's TEXT details to ESP32 |
| Push all to ESP32 | Send all TEXT records to ESP32 |
| Probe host | Check one configured TCP port. Not definitive ON/OFF |
| Probe all every 20 seconds | Repeated host TCP checks (in memory) |
| Wake selected | Request WOL, simulated unless ARMED; confirmation required |
| Shutdown selected | Request SSH shutdown, simulated unless ARMED; confirmation required |
| ARM real LAN power commands | Allow real commands for this GUI session only |
| Event log | Check errors, BLE activity and simulated/live requests |

For real WOL, configure a valid MAC and WOL support on the target computer.
For real shutdown, configure OpenSSH, matching host, SSH username, SSH private
key path and permission to shut down the selected PC. **Do not arm** for normal
GUI/image/microSD setup tests; leave commands simulated.

## 4. Red POWER button, sleep and true OFF

**Current hardware:** Red button shorts GPIO32 to GND. Holding it for 1.2 s
puts the ESP32 into **deep sleep**, not true power-off. Pressing it again wakes
via GPIO32. The update attempts to turn off the 1602 LCD backlight before
sleep; the ST7789 backlight remains lit if BL is hardwired to the 3.3V rail.
A powered TFT BL and the external modules still consume battery current.

**True electrical OFF requires additional switching hardware.** For keeping
this existing RED **momentary** button, choose a 5V-compatible push-on/push-off
power latch / soft-latching switch module with adequate load-current rating,
whose pushbutton is powered from the **battery side** so it can switch ON
when the ESP32 is fully unpowered. Conceptual layout:

```
Regulated 5V battery + ---> latch module VIN
Battery ground ----------> latch GND
Red momentary switch ----> latch button input (as module specifies)
Latch switched +5V ------> ESP32 DevKit 5V/VIN (verify board labeling)
                       +-> 5V-side 1602 LCD supply (if required)
ESP32 3V3 ---------------> verified 3.3V peripherals
All grounds --------------> common ground
```

**DO NOT** use the GPIO32-to-GND wiring for the same red button simultaneously
with a latch module's control input unless that module specifically documents
such wiring. Move the button to the external latch input and revise firmware
button behavior accordingly. A mechanical latching ON/OFF switch is simpler
but would require replacing the existing momentary red button.

**Do not connect an unregulated Li-ion cell directly to 5V/VIN or 3V3.** Use a
protected, regulated 5V battery supply. A USB power bank may shut itself off at
low current; check behavior with a latch controller and deep-sleep mode.

None of the above true-OFF latch circuits are included in v0.5; component and
wiring depend on the switch module you select. No hard power switch has been
built or validated. Avoid powering ESP32 from USB and 5V/VIN simultaneously
unless your exact board supports it.

## 5. Debugging

- GUI image shows but TFT image missing: image was not copied to microSD
  ROOT, avatar filename differs, BMP unsupported, SD read/wiring failed.
- TFT screen still bright after red POWER: BL wired to constant 3.3V remains on.
- LCD screen still lights: backpack may ignore backlight-off command, check it.
- SD init failed: check actual breakout's 3.3V supply requirement, MOSI GPIO23,
  MISO GPIO19, SCK GPIO18, CS GPIO13, FAT partition, shared SPI ground.
- GUI BLE disconnected: turn on PC Bluetooth, power ESP32, upload firmware;
  connect to `DirectoryConsole` before pushing.
- Offline editing works normally without microSD or BLE.

## 6. Limits

Prototype firmware and GUI have not been compiled or hardware-tested against
this exact ESP32/SD/TFT/LCD combination. GUI conversion/export logic tested
locally. An SD card cannot be physically formatted or copied here.
