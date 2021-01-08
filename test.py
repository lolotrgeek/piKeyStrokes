from hid import mouse 
from hid import keyboard
from main import ThreadedServer
from main import server_address
from main import server_port
from main import timeout

ThreadedServer(server_address,server_port, timeout).listen()

keyboard.send_keystroke(server_address, 0x0, 0x0)
keyboard.send_release_keys(server_address)

mouse.send_mouse_event(server_address, 0, 0 & 0xff, 0 & 0xff, 0 & 0xff)