import main

main.key_stroke(0x0, 0x0)
main.key_release()

movemouse = {
    "buttons": 0,
    "x" : 1, # move mouse 1 pixel to right
    "y" : 1, # move mouse 1 pixel up
    "wheel": 0,
}

main.mouse_event(movemouse)
