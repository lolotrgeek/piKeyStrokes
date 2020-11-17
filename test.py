import main

main.key_stroke(0x0, 0x04)
main.key_release()

# from request_parsers/mouse_events.py
@dataclasses.dataclass
class MouseEvent:
    # A bitmask of buttons pressed during the mouse event.
    buttons: int

    # A value from 0.0 to 1.0 representing the cursor's relative position on the
    # screen.
    relative_x: int
    relative_y: int

    # Wheel deltas can either be:
    # -1 - Scroll up.
    #  0 - Don't change scroll position.
    #  1 - Scroll down.
    vertical_wheel_delta: int
    horizontal_wheel_delta: int


movemouse = MouseEvent(
    buttons=0,
    relative_x=0.5,
    relative_y=0.5,
    vertical_wheel_delta=0,
    horizontal_wheel_delta=0,
)

main.mouse_event(movemouse)
