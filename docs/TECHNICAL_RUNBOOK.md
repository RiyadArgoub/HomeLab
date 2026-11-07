# Technical Runbook | Computer Directory Console

**Status:** Prototype. Physical and real-hardware integration not yet validated. Read entire power section before connecting devices.

## A. Inventory and electrical assumptions

- ESP32-WROOM-32 DevKit with accessible GPIO 13, 14, 16, 17, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33, 34, 35.
- ST7789V 2-inch **240 × 320** SPI TFT with pads `VCC GND DIN CLK CS DC RST BL`. Verify exact board's 3.3 V power and BL requirements. Modules with the same controller have different breakout backlights.
- 16×2 LCD with I²C backpack, common address `0x27` (some `0x3F`). A 5 V backpack may pull SDA/SCL up to **5 V**, which is **unsafe directly** for ESP32 GPIO. If so, use a suitable bidirectional I²C level shifter and separate 5 V supply connection to LCD side.
- 3.3 V-compatible SPI microSD adapter with six signals CS/SCK/MOSI/MISO/VCC/GND, formatted 1 GB FAT card. **Some 5 V-labeled modules do not work when powered at 3.3 V** because of their on-board level-shifting circuits. Use a true 3.3 V logic breakout.
- 2-axis joystick with VRx/VRy. Feed its VCC from 3V3 so ADC never sees 5 V. Leave SW unconnected.
- Four normally-open **square momentary** buttons. Each connects GPIO to GND, using ESP32 internal pull-ups.
- Small **passive**, low-current piezo (not a high-current active buzzer); connect GPIO27 to +, GND to −. Add a transistor driver if the selected buzzer needs more GPIO current.
- USB 5 V power from a quality supply, powering the ESP32 DevKit by USB. Common ground across modules. Power budget depends on TFT backlight and adapter, verify regulator capacity before mounting.
- Optional: 10 kΩ external pull-up on GPIO32 to 3V3 if deep-sleep wake isn't reliable with your board, or power-latch controller for true electrical OFF. These are **not** included in the base circuit.

## B. Authoritative pin map

| Unit | Terminal | ESP32 |
| --- | --- | --- |
| TFT | VCC | 3V3 only if board rated for it |
| TFT | GND | GND |
| TFT | DIN | GPIO23 SPI MOSI |
| TFT | CLK | GPIO18 SPI SCK |
| TFT | CS | GPIO16 |
| TFT | DC | GPIO17 |
| TFT | RST | GPIO14 |
| TFT | BL | **VERIFY** module electrical details, do not guess |
| microSD | VCC | 3V3 on compatible breakout |
| microSD | GND | GND |
| microSD | MOSI / DI | GPIO23 SPI MOSI |
| microSD | SCK / CLK | GPIO18 SPI SCK |
| microSD | MISO / DO | GPIO19 SPI MISO |
| microSD | CS | GPIO13 |
| I²C LCD | SDA | GPIO21 via level shifter if LCD side 5 V |
| I²C LCD | SCL | GPIO22 via level shifter if LCD side 5 V |
| I²C LCD | VCC | 3V3 only if known compatible, otherwise 5 V LCD side |
| I²C LCD | GND | GND |
| Joystick | VRx | GPIO34 |
| Joystick | VRy | GPIO35 |
| Joystick | VCC / GND | 3V3 / GND |
| Joystick | SW | leave unused |
| POWER RED | switch contacts | GPIO32 / GND |
| BACK YELLOW | switch contacts | GPIO33 / GND |
| PRESS GREEN | switch contacts | GPIO25 / GND |
| STOP BLUE | switch contacts | GPIO26 / GND |
| Passive piezo | + / − | GPIO27 / GND |

All SPI chip-selects must remain separate. A TFT with no MISO is write-only; SD provides MISO. If you have a different ESP32 model, **do not reuse this pin map blindly**.

## C. Physical wiring order (unpowered)

1. Verify USB disconnected, measure breadboard red/blue rail continuity and any gaps.
2. Make common GND. Add one module at a time, beginning with TFT (verified 3.3 V logic/power).
3. Wire display SPI: MOSI=23, SCK=18, CS=16, DC=17, RST=14, GND; leave BL unconnected until its requirements are known. Some boards require BL to be powered to see an image.
4. Wire microSD: share MOSI and SCK; use separate CS=13 and MISO=19.
5. Wire I²C LCD on 21/22 through a shifter if its signals are at 5 V. Do not join 5 V and 3V3 rails.
6. Wire joystick analog outputs 34/35, power 3V3. SW is unused.
7. Wire four buttons to their GPIO pins and GND. For 4-leg tactile switches, check the paired contacts with a multimeter first. No external pull-up needed in base circuit.
8. Wire passive piezo and verify its rated current.
9. With USB still disconnected, inspect for bare leads touching. Perform continuity/short checks between 3V3 and GND and against any 5 V rail.
10. First boot one board at a time. Confirm pin/supply measurements before making everything permanent.

## D. MicroSD layout and data protocol

Card root must have:

```
/computers.csv
/placeholder.bmp
```

CSV format is **pipe-separated** (not comma-separated):

```
name|role|host|mac|avatar.bmp|UNKNOWN|notes
```

The firmware parses up to 12 records. Keep text fields short and do not insert pipes or newlines. The desktop manager maintains `assets/computers.json`, while BLE `SYNC` updates the ESP32 microSD copy. On reboot, status is forced to `UNKNOWN` until refreshed: stored `ONLINE` is not trusted.

BMP requirements: uncompressed **24-bit**, **120 × 120 pixels**; filenames lower-case; place at card root. You can rebuild generic placeholder assets by running `python assets/make_avatars.py`. Provided SVG files can be edited in vector graphics software.

## E. Menu state machine

```
Directory (joystick up/down, PRESS selects)
  └─ Detail: portrait + role + cached status + description
       ├─ PRESS → send WAKE request → Result
       ├─ BACK  → Directory
       └─ STOP  → Confirm NO/YES
                   ├─ NO  → Detail (no action)
                   └─ YES → 3×3 keypad digits 1–9
                              PIN test: 1 2 3 4
                              └─ Select target:
                                   ├─ Selected computer
                                   └─ ALL registered computers
                                       └─ Send STOP request to Python manager
                                             (manager unarmed by default; operator confirms)
```

- `BACK` on Directory: error chirp only (no menu above it).
- `PRESS` in wrong state: error chirp.
- `POWER` held about 1.2 seconds: ESP32 deep sleep; RTC GPIO32 button wakes it. This is **soft sleep only**. The board's regulator, backlight and module circuitry remain energized. True power cut requires power latch hardware and redesign.
- `STOP` is a remotely delivered **graceful shutdown request**. **It is not a safety-rated stop** and cannot guarantee immediate stop or act if network/manager is down.
- Current keypad password `1234` is openly included for demo. No rate limit or BLE pairing implemented. Never protect real production infrastructure with this build as-is.

## F. BLE UART-like protocol

The BLE peripheral advertises `DirectoryConsole`. A Linux, Windows or macOS desktop with Bleak connects as central.

Service UUID: `f23a0001-6cf8-4c4c-a3f2-120c95e7ca13`

- RX (PC → ESP32, write): `f23a0002-6cf8-4c4c-a3f2-120c95e7ca13`
- TX (ESP32 → PC, notify): `f23a0003-6cf8-4c4c-a3f2-120c95e7ca13`

Messages are UTF-8 ASCII-friendly **newline-delimited** frames, split into BLE chunks of at most 20 bytes for broad MTU compatibility. Do not split a single logical line across unrelated clients.

| Direction | Example | Description |
| --- | --- | --- |
| GUI → ESP32 | `PING` | ESP32 replies `HELLO` |
| GUI → ESP32 | `SYNC|0|Heather-PC1|AI|192.168.2.101||placeholder.bmp|UNKNOWN|Test computer` | Replace a cached record; saved to SD |
| GUI → ESP32 | `STATE|0|ONLINE` | Update the display's live status; not persisted as ONLINE |
| ESP32 → GUI | `REQ|0|WAKE` | Request Wake-on-LAN for selected record |
| ESP32 → GUI | `REQ|ALL|STOP` | Request graceful shutdown for all, GUI approval required |
| GUI → ESP32 | `ACK|0|WAKE|SIM` | Simulated, not actually executed |
| GUI → ESP32 | `ACK|0|STOP|OK` | SSH command sent; not proof powered down |

The manager must be running, BLE connected, and **manually armed** for real shutdown. The manager asks for a final human confirmation on each request. For hardware deployment, replace this prototype BLE scheme with authenticated/encrypted BLE and audit logging.

## G. Desktop management runbook

1. Install Python 3.10+, Tkinter, and `pip install -r python_gui/requirements.txt`.
2. Launch `python python_gui/console_manager.py`. It opens and edits local JSON even when BLE unavailable.
3. Select a test entry; set a *real* hostname/IP, role, optional description and real MAC for WOL. Save.
4. Click **Probe host** to test a configured service port (default 22). `ONLINE` means the port accepted a connection. `UNVERIFIED` could mean off, firewall, or no service; never equate it with `OFF`.
5. Flash ESP32 and click **Connect Bluetooth**. The ESP32 device name is `DirectoryConsole`. Use `Push all` after connecting to update SD records.
6. To test without altering real hosts, leave **ARM** unchecked, click **Wake selected** or **Shutdown selected**, approve simulation and check logs. Never mistake SIM for successful remote power action.
7. For Wake-on-LAN, enable WOL in motherboard BIOS/UEFI and NIC OS config, verify the local subnet/broadcast and MAC. Then arm manager for the session and authorize a specific WAKE request. WOL packet sent ≠ confirmed boot.
8. To use SSH shutdown, configure `ssh_user`, absolute `ssh_key` path (point to your existing private key outside repo), `host`, `platform`; ensure SSH host key is known and OS user has just the necessary shutdown permission. Arm and approve only on a noncritical test machine.
9. Never enable real shutdown actions on production systems before adding per-device roles, audit logging, physical controls, and authentication.

Linux default SSH remote command is fixed `sudo -n /usr/bin/systemctl poweroff`. Windows OpenSSH version is `shutdown /s /t 0`. The Python manager uses host validation and an argument list rather than concatenating arbitrary shell snippets. Connections are authenticated by existing SSH key and known-hosts policy. Windows OpenSSH service and remote account permissions must be set up separately.

## H. Troubleshooting

| Problem | First check |
| --- | --- |
| TFT stays dark | VCC/GND; TFT BL electrical requirements, hardware SPI pins, display rotation/init |
| LCD blank | I²C address 0x27 vs 0x3F, contrast potentiometer on backpack, 3.3/5 V and I²C level-shifting |
| SD fails | Use real 3.3 V SPI breakout, verify card FAT formatting, distinct CS13 and TFT CS16 |
| Portrait box only | Correct `/name.bmp` root location, 24-bit uncompressed 120×120 BMP |
| Joystick reversed | Change `INVERT_X` or `INVERT_Y` in firmware, calibrate with joystick centered |
| Square buttons ignored | Use opposite switch contacts; continuity test, GND rail and GPIO numbering |
| POWER does not physically shut off | Expected. It is deep sleep, not load power switch; BL can remain illuminated |
| No BLE device found | ESP32 BLE advertising, computer Bluetooth enabled, Linux BlueZ permissions, no second connection |
| GUI works but no PC powers on | Verify manager is armed, requests approved, actual MAC/host, WOL and SSH preconditions |
| "UNVERIFIED" host | TCP probe couldn't connect; cannot conclude PC is OFF |

## I. Validation checklist

- [ ] Measure actual board and switch dimensions.
- [ ] Verify TFT VCC/BL and LCD backpack logic voltage.
- [ ] Compile ESP32 sketch with installed exact board and libraries.
- [ ] Confirm Serial Monitor startup + microSD read.
- [ ] Confirm each of five `.bmp` images is shown.
- [ ] Confirm four buttons + joystick axes via interaction.
- [ ] Confirm malformed PIN doesn't send shutdown requests.
- [ ] Confirm BLE disconnect shows offline status.
- [ ] Confirm GUI offline edit/save/reload.
- [ ] Confirm BLE `SYNC` and `ACK` against real ESP32.
- [ ] Confirm **unarmed** STOP only simulates and never runs SSH.
- [ ] Confirm all-target shutdown requires GUI human approval when armed.
- [ ] Verify physical mounting and insulation before soldering.

**Only code/unit tests and model integrity checks have been run here, not actual board, BLE, or host shutdown integration tests.**
