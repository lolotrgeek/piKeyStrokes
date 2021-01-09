from hid import mouse
from hid import keyboard
from main import ThreadedServer
from main import server_address
from main import server_port
from main import timeout

ThreadedServer(server_address, server_port, timeout).listen()

#Keyboard
keyboard.send_keystroke(server_address, 0x0, 0x0)
keyboard.send_release_keys(server_address)

# Mouse
test = b'\x01\xff\x3f\xff\x5f\x00'

# https://github.com/mtlynch/tinypilot/blob/master/app/tests/hid/test_mouse.py
# Byte 0   = Button 1 pressed
# Byte 1-2 = 32767 * 0.5 = 16383.5 = 0x3fff
# Byte 3-4 = 32767 * 0.75 = 24575.25 = 0x5fff
mouse.send_mouse_event(server_address, 0, 0 & 0xff, 0 & 0xff, 0 & 0xff)
