"""Tests for image import and card export without a GUI or ESP32."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python_gui'))
from media_tools import import_portrait, export_sd_card, avatar_filename

class MediaTests(unittest.TestCase):
    def test_custom_image_and_export(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            source = home / 'user_photo.jpg'
            Image.new('RGB', (720, 380), (20, 50, 100)).save(source)
            name = import_portrait(source, 'pc01.bmp', home / 'avatars')
            self.assertEqual(name, 'pc01.bmp')
            with Image.open(home/'avatars'/'pc01.bmp') as picture:
                self.assertEqual(picture.mode, 'RGB')
                self.assertEqual(picture.size, (120, 120))
                self.assertEqual(picture.format, 'BMP')
            with Image.open(home/'avatars'/'pc01.png') as picture:
                self.assertEqual(picture.size, (300, 300))
            records=[{'name':'TEST-PC','role':'NAS','host':'192.0.2.8','avatar':'pc01.bmp','mac':'','notes':'demo'}]
            count, images=export_sd_card(records, home/'sdcard', home/'avatars')
            self.assertEqual((count,images),(1,1))
            self.assertEqual((home/'sdcard'/'computers.csv').read_text(), 'TEST-PC|NAS|192.0.2.8||pc01.bmp|UNKNOWN|demo\n')
            self.assertTrue((home/'sdcard'/'pc01.bmp').exists())
            self.assertFalse((home/'sdcard'/'pc01.png').exists())

    def test_invalid_file_path_rejected(self):
        for bad in ('../heather.bmp', 'ninetitle.bmp', '/tmp/a.bmp', 'hi.png', ''):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):avatar_filename(bad)

    def test_sample_card_layout(self):
        records=json.loads((ROOT/'assets'/'computers.json').read_text())
        with tempfile.TemporaryDirectory() as target:
            count, images=export_sd_card(records, target, ROOT/'assets'/'avatars')
            self.assertEqual((count,images),(5,5))
            self.assertEqual(len(list(Path(target).iterdir())),6)

if __name__=='__main__':unittest.main()
