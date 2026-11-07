"""Smoke tests for offline data, assets, CAD and GUI control protocol."""
import sys
import unittest
from pathlib import Path
from PIL import Image
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'python_gui'))
from console_manager import load_records,sync_message,clean_field
from remote import wake_on_lan,probe_tcp

class SmokeTests(unittest.TestCase):
    def test_sample_computers(self):
        r=load_records();self.assertEqual(len(r),5)
        self.assertEqual([x['name'] for x in r],['Heather-PC1','Lindsay-PC2','Zoey-PC3','Gwen-PC4','Courtney-PC5'])
    def test_sync_frame(self):
        s=sync_message(0,load_records()[0]);self.assertTrue(s.startswith('SYNC|0|Heather-PC1|AI|'))
        self.assertIn('placeholder.bmp',s)
    def test_safe_pipe_encoding(self):
        self.assertEqual(clean_field('A|B\nC'),'A/ B C'.replace('/ ','/'))
    def test_bmp_assets(self):
        files=sorted(p.name for p in (ROOT/'assets'/'avatars').iterdir())
        self.assertEqual(files,['placeholder.bmp','placeholder.png','placeholder.svg'])
        with Image.open(ROOT/'assets'/'avatars'/'placeholder.bmp') as im:
            self.assertEqual(im.size,(120,120))
            self.assertEqual(im.mode,'RGB')
    def test_wol_invalid_mac_rejected(self):
        with self.assertRaises(ValueError):wake_on_lan('00:11:22')
    def test_stl_watertight(self):
        import trimesh
        for p in (ROOT/'stl').glob('*.stl'):
            with self.subTest(p.name):
                m=trimesh.load(p,force='mesh')
                self.assertTrue(m.is_watertight)
                self.assertGreater(m.volume,0)
    def test_schematic_valid_xml(self):
        import xml.etree.ElementTree as ET
        root=ET.parse(ROOT/'schematics'/'Directory_Interconnect.sch').getroot()
        self.assertEqual(root.tag,'eagle')
        self.assertGreaterEqual(len(root.findall('.//net')),15)

if __name__=='__main__':unittest.main()
