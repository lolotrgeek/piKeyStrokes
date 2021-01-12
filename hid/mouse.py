from hid import write as hid_write
from hid import send as hid_send

# Reference:
# https://github.com/mtlynch/tinypilot/commit/ea853b54fa56ce275b6f776caa5a839451013e84#diff-d589676c00c019dfd703ad4aac7f458ffe5efda9116a930d3474d28aa3def657
# https://www.raspberrypi.org/forums/viewtopic.php?t=234495
# https://wiki.osdev.org/Mouse_Input

def send_mouse_event(server_address, button, dx, dy, wheel):
    event = [button, dx, dy, wheel]
    hid_send.send(server_address, event) 

def send_mouse_event_relative(server_address, button, x, y, wheel, height, width):
    report = [button, x & 0xff, y & 0xff, wheel & 0xff, height & 0xff, width & 0xff]
    hid_send.send(server_address, report)
    
def write_mouse_event(mouse_path, event):
    report = event 
    hid_write._write_to_hid_interface_immediately(mouse_path, report)

def write_mouse_event_relative(mouse_path, event):
    '''
    Scale mouse events with a relative coordinate system.

    When recorded the x,y values are the float of a coord divided by height for x and width for y

    This allows the system to adapt to changing screen sizes and convert pixel values to movements

    NOTE: requires 2-byte `x , y` inputs, see `enable_hid.sh` `Mouse 2`
    '''
    x , y , height, width = event[1], event[2], event[4], event[5]   
    print(x, y, height, width)

    relative_x = set_relative(x, width)
    relative_y = set_relative(y, height)
    scale_x, scale_y = scale_mouse_coordinates(relative_x, relative_y)

    report = [0] * 6
    report[0] = event[0] # button
    report[1] = scale_x & 0xff 
    report[2] = (scale_x >> 8) & 0xff
    report[3] = scale_y & 0xff
    report[4] = (scale_y >> 8) & 0xff
    report[5] = event[3] # wheel   

    hid_write._write_to_hid_interface_immediately(mouse_path, report)

def set_relative(coord, total):
    return min(1.0, max(0.0, coord / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y