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
To run a HID event listener set `server_address` in `main.py` and run:

```
python main.py
```

For the client to send HID events to the listener see `test.py` for example commands.

## Notes
Since the HID gadget will unmount on reboot the purpose of the service created on install is to re-initialize the HID gadget on boot (think of it like plugging the device in) the service is created in `setup.sh` and `enable_hid.service`.


## Reference
install script from: 

[pi-as-keyboard](https://github.com/c4software/pi-as-keyboard)

HID descriptor based on:

[init-gadget-script](https://github.com/mtlynch/tinypilot/blob/33d3cd5630ea17c4ce02eb436f0cdf436d72ac0a/scripts/usb-gadget/init-usb-gadget)

[eleccelerator](https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/)