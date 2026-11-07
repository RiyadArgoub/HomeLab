"""User image conversion and microSD export utilities for Directory Console.

Imports convert common photo formats to the original firmware's exact supported
120x120 uncompressed 24-bit BMP and a desktop PNG preview. No image BLE transfer.
"""
import re
import shutil
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
AVATARS = ROOT / 'assets' / 'avatars'
SD_FILENAME = re.compile(r'^[A-Za-z0-9_-]{1,31}\.bmp$', re.IGNORECASE)
MAX_FIRMWARE_PCS = 128


def avatar_filename(value):
    filename = str(value or '').strip()
    if Path(filename).name != filename or not SD_FILENAME.fullmatch(filename):
        raise ValueError('Avatar filename must be a simple BMP filename (letters, numbers, _ or -, up to 31 characters), such as heather1.bmp')
    return filename.lower()


def import_portrait(source, avatar_name, avatar_dir=AVATARS):
    """Crop to square and convert to PNG (GUI) + RGB 24-bit BMP (ESP32)."""
    target_name = avatar_filename(avatar_name)
    stem = Path(target_name).stem
    avatar_dir = Path(avatar_dir)
    avatar_dir.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source) as raw:
            img = ImageOps.exif_transpose(raw).convert('RGB')
            # Contain + crop avoids stretching portraits of unusual proportions.
            square = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)
            display = square.copy()
            device = square.resize((120, 120), Image.Resampling.LANCZOS)
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        raise ValueError(f'Cannot read this image: {exc}') from exc
    # Pillow uses uncompressed Windows RGB BMP for mode='RGB'.
    display.save(avatar_dir / (stem + '.png'), 'PNG')
    device.save(avatar_dir / target_name, 'BMP')
    return target_name


def export_sd_card(records, output, avatar_dir=AVATARS):
    """Export the ESP32's root folder files. Never formats or deletes card files.

    Export ONLY what the ESP32 uses; no JSON, SVG, large PNGs or SSH keys.
    Overwrites computers.csv and the named BMPs in output if they exist.
    """
    output = Path(output)
    avatar_dir = Path(avatar_dir)
    if not 1 <= len(records) <= MAX_FIRMWARE_PCS:
        raise ValueError('Firmware supports between 1 and 128 computer records')
    lines = []
    avatars = []
    names_seen = set()
    for index, rec in enumerate(records):
        avatar = avatar_filename(rec.get('avatar', ''))
        if avatar in names_seen:
            # Sharing one portrait between computers is fine; avoid copy twice.
            pass
        else:
            path = avatar_dir / avatar
            if not path.is_file():
                raise FileNotFoundError(f'Missing ESP32 image: {path}. Use Choose portrait first.')
            with Image.open(path) as img:
                if img.size != (120, 120) or img.mode != 'RGB' or img.format != 'BMP':
                    raise ValueError(f'{path.name} must be uncompressed 120x120 24-bit RGB BMP')
                compression = img.info.get('compression', 0)
                if compression not in (None, 0):
                    raise ValueError(f'{path.name} is compressed; import it using Choose portrait')
            avatars.append((path, avatar))
            names_seen.add(avatar)
        def clean(v):
            return str(v or '').replace('|','/').replace('\n',' ').replace('\r',' ').strip()
        fields = [rec.get('name',''), rec.get('role',''), rec.get('host',''),
                  rec.get('mac',''), avatar, 'UNKNOWN', rec.get('notes','')]
        if not clean(fields[0]):
            raise ValueError(f'Computer record {index+1} has no name')
        line = '|'.join(clean(x) for x in fields)
        if len(line.encode('utf-8')) > 230:
            raise ValueError(f'Computer {index+1} fields are too long for reliable BLE sync')
        lines.append(line)
    output.mkdir(parents=True, exist_ok=True)
    for path, name in avatars:
        dst = output / name
        if path.resolve() != dst.resolve():
            shutil.copyfile(path, dst)
    (output / 'computers.csv').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return len(lines), len(avatars)
