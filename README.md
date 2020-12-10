# PiKeyStrokes Library
Enables HID emulation by enabling OTG on RPi4 or RPiZero/W.

## Install
The `install/enable_hid.sh` script enables two HID devices:
- `hid0` : is a keyboard, which typically registers at `/dev/hidg0/`
- `hid1` : is a mouse, which typically registers at `/dev/hidg1/`

```
$ sudo ./install/setup.sh
$ sudo reboot
```

## Usage
See `main.py` for following functions: 

### Key_stroke(hid_keycode, modifiers)
Press the given key with any modifiers

> hid_keycode - type : `buf`

keycodes can be found in the `/hid/keycodes` directory of this repo

> modifiers - type : `buf`


```
# press 'ctrl + c'
key_stroke(0x06, 0xe0)
```

### mouse_event(mouse_move_event)
Move mouse, press buttons, roll scrollwheel
> mouse_move_event - type : `dict`

see `test.py` for how to build a `mouse_move_event`

## TODO
- consider vars not dict for mouse_event
- make this a pypi package

