"""Prepare SD root files from desktop registry: python tools/prepare_sd.py --output sd_card"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python_gui'))
from media_tools import export_sd_card

p=argparse.ArgumentParser(description='Export computers.csv and 120x120 24-bit BMP portraits for the ESP32 microSD.')
p.add_argument('--output', required=True, help='Folder for SD card files. Existing matching files are overwritten.')
p.add_argument('--registry', default=str(ROOT/'assets'/'computers.json'))
p.add_argument('--avatars', default=str(ROOT/'assets'/'avatars'))
a=p.parse_args()
records=json.loads(Path(a.registry).read_text(encoding='utf-8'))
count, images=export_sd_card(records, Path(a.output), Path(a.avatars))
print(f'Prepared {count} computer(s) and {images} BMP portraits in {a.output}')
print('Copy contents to the ROOT of a FAT16/FAT32 microSD card; BLE does not carry portraits.')
