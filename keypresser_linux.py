from evdev import uinput, ecodes

KEY_LETTERS = [
    ecodes.KEY_A,
    ecodes.KEY_B,
    ecodes.KEY_C,
    ecodes.KEY_D,
    ecodes.KEY_E,
    ecodes.KEY_F,
    ecodes.KEY_G,
    ecodes.KEY_H,
    ecodes.KEY_I,
    ecodes.KEY_J,
    ecodes.KEY_K,
    ecodes.KEY_L,
    ecodes.KEY_M,
    ecodes.KEY_N,
    ecodes.KEY_O,
    ecodes.KEY_P,
    ecodes.KEY_Q,
    ecodes.KEY_R,
    ecodes.KEY_S,
    ecodes.KEY_T,
    ecodes.KEY_U,
    ecodes.KEY_V,
    ecodes.KEY_W,
    ecodes.KEY_X,
    ecodes.KEY_Y,
    ecodes.KEY_Z
]

KEY_DIGITS = [
    ecodes.KEY_0,
    ecodes.KEY_1,
    ecodes.KEY_2,
    ecodes.KEY_3,
    ecodes.KEY_4,
    ecodes.KEY_5,
    ecodes.KEY_6,
    ecodes.KEY_7,
    ecodes.KEY_8,
    ecodes.KEY_9
]

ui = uinput.UInput()

def type_letter(letter):
    scancode   = 0
    is_shifted = False

    digit_symbols = ")!@#$%^&*("

    if letter.islower():
        scancode = KEY_LETTERS[ord(letter) - ord('a')]
    elif letter.isdigit():
        scancode = KEY_DIGITS[ord(letter) - ord('0')]
    elif letter.isupper():
        scancode = KEY_LETTERS[ord(letter.lower()) - ord('a')]
        is_shifted = True
    elif letter in digit_symbols:
        scancode = KEY_DIGITS[digit_symbols.index(letter)]
        is_shifted = True

    # press
    if is_shifted:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
    ui.write(ecodes.EV_KEY, scancode, 1)
    ui.syn()

    # release
    if is_shifted:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
    ui.write(ecodes.EV_KEY, scancode, 0)
    ui.syn()