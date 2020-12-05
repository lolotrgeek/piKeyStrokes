from main import key_stroke

def Copy():
    key_stroke(0x06, 0xe0)

def Paste():
    key_stroke(0x13, 0xe0)

def Modified(key):
    key_stroke(key, 0xe1)

def Press(key):
    key_stroke(key,0x0)