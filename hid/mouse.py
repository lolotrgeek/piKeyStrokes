from hid import write as hid_write

# Reference:
# https://github.com/mtlynch/tinypilot/commit/ea853b54fa56ce275b6f776caa5a839451013e84#diff-d589676c00c019dfd703ad4aac7f458ffe5efda9116a930d3474d28aa3def657
# https://www.raspberrypi.org/forums/viewtopic.php?t=234495
# https://wiki.osdev.org/Mouse_Input

def send_mouse_event(mouse_path, button, dx, dy, wheel):
    report = [button, dx & 0xff, dy & 0xff, wheel & 0xff]
    hid_write._write_to_hid_interface(mouse_path, report)