import logging
import os

from hid import keyboard as fake_keyboard
from hid import mouse as fake_mouse
from hid import write as hid_write

# from hid.keycodes import azerty
# from hid.keycodes import norwegian
# from hid.keycodes import qwerty
# from hid.keycodes import modifiers


logger = logging.getLogger(__name__)
# Location of file path at which to write keyboard HID input.
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
# Location of file path at which to write mouse HID input.
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
# Keyboard layout on target computer.
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')

def key_stroke(hid_keycode, modifiers):
    try:
        fake_keyboard.send_keystroke(keyboard_path, hid_keycode, modifiers)
    except hid_write.WriteError as e:
        logger.error('Failed to write key: %s (keycode=%d). %s', hid_keycode,e)
        return {'success': False}
    return {'success': True}


def mouse_event(mouse_move_event):
    try:
        fake_mouse.send_mouse_event(mouse_path, mouse_move_event.buttons,
                                    mouse_move_event.relative_x,
                                    mouse_move_event.relative_y,
                                    mouse_move_event.vertical_wheel_delta,
                                    mouse_move_event.horizontal_wheel_delta)
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}

def key_release():
    try:
        fake_keyboard.release_keys(keyboard_path)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)

# def main():
#     return

# if __name__ == '__main__':
#     main()