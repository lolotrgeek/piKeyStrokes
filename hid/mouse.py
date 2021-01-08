from hid import write as hid_write
from hid import send as hid_send

# Reference:
# https://github.com/mtlynch/tinypilot/commit/ea853b54fa56ce275b6f776caa5a839451013e84#diff-d589676c00c019dfd703ad4aac7f458ffe5efda9116a930d3474d28aa3def657
# https://www.raspberrypi.org/forums/viewtopic.php?t=234495
# https://wiki.osdev.org/Mouse_Input

def receive_mouse_event(mouse_path, event):
    report = event
    if isinstance(event[1], float):
        x, y = scale_mouse_coordinates(event[1], event[2])
        report[1] = x
        report[2] = y        
    hid_write._write_to_hid_interface_immediately(mouse_path, report)

def send_mouse_event(server_address, button, dx, dy, wheel):
    event = [button, dx, dy, wheel]
    hid_send.send(server_address, event)    

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 127.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y