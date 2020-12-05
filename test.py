import main

main.key_stroke(0x0, 0x0)
main.key_release()

movemouse = {
    "buttons": 0,
    "relative_x" : 0.5,
    "relative_y" : 0.5,
    "vertical_wheel_delta": 0,
    "horizontal_wheel_delta": 0,
}

main.mouse_event(movemouse)
