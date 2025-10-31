import argparse
from PIL import Image
import re

def location(filename: str) -> None:
    try:
        with Image.open(filename) as img:
            exif = img.getexif()
    except Exception:
        print('No location info')
        return

    if not exif:
        print('No location info')
        return

    try:
        gps = exif.get_ifd(34853)
        lat_dms = gps[2]
        lon_dms = gps[4]
        lat_ref = gps.get(1)
        lon_ref = gps.get(3)

        def _rat(x):
            try:
                return float(x.numerator) / float(x.denominator)
            except AttributeError:
                return float(x[0]) / float(x[1]) if isinstance(x, (tuple, list)) else float(x)

        def _dms_to_dd(dms, ref):
            deg, minu, sec = _rat(dms[0]), _rat(dms[1]), _rat(dms[2])
            dd = deg + minu/60.0 + sec/3600.0
            if (isinstance(ref, bytes) and ref in (b'S', b'W')) or ref in ('S', 'W'):
                dd = -dd
            return dd

        lat_dd = _dms_to_dd(lat_dms, lat_ref)
        lon_dd = _dms_to_dd(lon_dms, lon_ref)

        print(f'Lat/Lon: ({lat_dd:.3f}) / ({lon_dd:.3f})')

    except Exception:
        print('No location info')


def pgp(filename: str) -> None:
    try:
        with open(filename, 'rb') as fh:
            data = fh.read()
        eoi = data.find(b'\xff\xd9')
        tail = data[eoi+2:] if eoi != -1 else b''
        text = tail.decode('utf-8', errors='ignore')

        m = re.search(r'-----BEGIN PGP.*?-----\s.*?-----END PGP.*?-----',
                      text, re.DOTALL)
        if m:
            print(m.group(0))
        else:
            print('No PGP Key found')
    except Exception:
        print('No PGP Key found')


def main():
    parser = argparse.ArgumentParser(description="Inspector Image")
    parser.add_argument('-map',  type=str, help='Location where the image was taken')
    parser.add_argument('-steg', type=str, help='Pgp key')
    args = parser.parse_args()

    if args.map:
        location(args.map)
    if args.steg:
        pgp(args.steg)


if __name__ == "__main__":
    main()
