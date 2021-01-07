import logging
import os
import socket
import threading
import sys

from hid import keyboard as fake_keyboard
from hid import mouse as fake_mouse
from hid import write as hid_write

# (IP, port)
server_address = 'localhost'
server_port = 10000

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

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        print('Listening...')
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            print('Connected.')
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:
            try:
                data = client.recv(16)
                if data:
                    size = sys.getsizeof(data)
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
                    
                else:
                    print('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    ThreadedServer(server_address,server_port).listen()    