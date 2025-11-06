#!/usr/bin/env python3
import hid
import sys

VID = 0x352F
PID = 0x0104

def build_led_report(on: bool, mode: int) -> bytes:
    on_off = 1 if on else 0
    if not on:
        mode = 0
    chk = (0xFE7B - mode + (1 - on_off)) & 0xFFFF

    rep = bytearray(64)
    rep[0]  = 0x4B
    rep[1]  = 0xC4
    rep[2]  = 0x0F
    rep[3]  = 0x00
    rep[4]  = 0x00
    rep[5]  = 0x03
    rep[6]  = 0x36
    rep[7]  = 0x20
    rep[8]  = on_off
    rep[9]  = 0x00
    rep[10] = 0x38
    rep[11] = 0x20
    rep[12] = mode & 0xFF
    rep[13] = (mode >> 8) & 0xFF
    rep[14] = chk & 0xFF
    rep[15] = (chk >> 8) & 0xFF
    return bytes(rep)

def find_pd200x_path():
    for dev in hid.enumerate(VID, PID):
        if dev.get('interface_number', -1) == 3 or dev.get('usage_page', 0) == 0xFF01:
            return dev['path']
    return None

def send_report(on: bool, mode: int):
    path = find_pd200x_path()
    if not path:
        raise RuntimeError("Не найден HID-интерфейс PD200X (права/udev?)")

    d = hid.device()
    try:
        d.open_path(path)
        data = build_led_report(on, mode)

        n = d.write(data)
        if n != len(data):
            raise RuntimeError(f"hid.write вернул {n} байт из {len(data)}")
    finally:
        try:
            d.close()
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: maono_pd200x_led.py off | 0..8")
        sys.exit(1)
    if sys.argv[1].lower() == "off":
        send_report(False, 0)
    else:
        m = int(sys.argv[1])
        if not (0 <= m <= 8):
            raise SystemExit("mode must be 0..8")
        send_report(True, m)
    print("OK")

