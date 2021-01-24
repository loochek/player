# roll events
# examples:
# [0, 0.12] // time to sleep
# [1, "SDFd"] // keys to press
# [2, "SADq"] // keys to release

EVENT_SLEEP       = 0
EVENT_KEY_PRESS   = 1
EVENT_KEY_RELEASE = 2

# EVENT_KEY_RELEASE is quite useless because we can't hold keys. Some notes of virtual keyboard is called with
# shift, so we can't hold several keys pressed at one time