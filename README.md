# PiKeyStrokes Library - Remote
Enables HID emulation by enabling OTG on RPi4 or RPiZero/W. Remote variant accepts inputs over TCP socket and writes them to HID interface.

## Install
The `install/enable_hid.sh` script enables two HID devices:
- `hid0` : is a keyboard, which typically registers at `/dev/hidg0/`
- `hid1` : is a mouse, which typically registers at `/dev/hidg1/`

```
$ sudo ./setup.sh
$ sudo reboot
```

## Uninstall
To uninstall simply disable the service and reboot. 
```
systemctl disable enable_hid.service
sudo reboot
```

## Usage
Set `server_address` in `main.py`.

```
python main.py
```

## API
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
- buttons
    - `0` - none
    - `1` - left 
    - `2` - right 
    - `4` - middle
- x
    - `int` in range `[-127, 127]`
- y
    - `int` in range `[-127, 127]`

- wheel 
    - `-1`- down
    - `0` - none
    - `1` - up

see `test.py` for how to build a `mouse_move_event`

## Notes

Since the HID gadget will unmount on reboot the purpose of the service is to re-initialize the HID gadget on boot (think of it like plugging the device in) the service is created in `setup.sh` and `enable_hid.service`.

## TODO
- consider vars not dict for mouse_event
- make this a pypi package

## Reference
install script from [pi-as-keyboard](https://github.com/c4software/pi-as-keyboard)

gadget init scrript from [init-gadget-script](https://github.com/mtlynch/tinypilot/blob/master/scripts/usb-gadget/init-usb-gadget)