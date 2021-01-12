import logging
import os
import socket
import threading
import sys

from hid import keyboard
from hid import mouse
from hid import write as hid_write

server_address = '192.168.1.248'
server_port = 10000
timeout = 60

logger = logging.getLogger(__name__)
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
mouse_2_path = os.environ.get('MOUSE_PATH', '/dev/hidg2')
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')


def key_stroke(key_event):
    try:
        keyboard.write_keystroke(keyboard_path, key_event)
    except hid_write.WriteError as e:
        logger.error('Failed to write key: %s (keycode=%d). %s', key_event,e)
        return {'success': False}
    return {'success': True}


def mouse_handler(mouse_event):
    try:
        if len(mouse_event) == 4 :
            print('Absolute', mouse_event)
            mouse.write_mouse_event(mouse_path, mouse_event)
        else:
            print('Relative:', mouse_event)
            mouse.write_mouse_event(mouse_2_path, mouse_event)
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}

def key_release():
    try:
        keyboard.release_keys(keyboard_path)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)

# https://stackoverflow.com/a/23828265
class ThreadedServer(object):
    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        print('Listening...')
        while True:
            client, address = self.sock.accept()
            client.settimeout(self.timeout)
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
                        mouse_handler(data)
                    # send data back for verification
                    client.sendall(data)
                else:
                    raise print('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    ThreadedServer(server_address,server_port, timeout).listen()    