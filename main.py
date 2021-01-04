import logging
import os
import socket
import sys

from hid import keyboard as fake_keyboard
from hid import mouse as fake_mouse
from hid import write as hid_write

# (IP, port)
server_address = ('localhost', 10000)

logger = logging.getLogger(__name__)
# Location of file path at which to write keyboard HID input.
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
# Location of file path at which to write mouse HID input.
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
# Keyboard layout on target computer.
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')


def key_stroke(key_event):
    try:
        fake_keyboard.receive_keystroke(keyboard_path, key_event)
    except hid_write.WriteError as e:
        logger.error('Failed to write key: %s (keycode=%d). %s', key_event,e)
        return {'success': False}
    return {'success': True}


def mouse_event(mouse_move_event):
    try:
        fake_mouse.receive_mouse_event(mouse_path, mouse_move_event)
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}

def key_release():
    try:
        fake_keyboard.release_keys(keyboard_path)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
# Wait for a connection
print('waiting for a connection')
connection, client_address = sock.accept()
try:
    print('connection from', client_address)
    # Receive the data in small chunks and retransmit it
    while True:
            data = connection.recv(16)
            if data:
                size = sys.getsizeof(data)
                print(size)
                if size == 25:
                    if data == bytearray([0] * 8):
                        # print('Release Keys', data)
                        key_release()
                    else: 
                        # print('Write Key', data)
                        key_stroke(data)
                else:
                    # print('Write Mouse', data)
                    mouse_event(data)
                
                # print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no more data from', client_address)
                break
finally:
    connection.close()