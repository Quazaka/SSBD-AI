import time
from directkeys import PressKey, ReleaseKey, O, W, A, S, D, SPACE


# Wait and print x seconds before proceeding.
def countdown(x):
    i = x
    while i > 0:
        print("Countdown: %d" % i)
        time.sleep(1)
        i -= 1


# Loop movement keys
def testMovement():
        while True:
            PressKey(O)

            PressKey(W)
            time.sleep(0.3)
            ReleaseKey(W)

            PressKey(D)
            time.sleep(0.3)
            ReleaseKey(D)

            PressKey(S)
            time.sleep(0.3)
            ReleaseKey(S)

            PressKey(A)
            time.sleep(0.3)
            ReleaseKey(A)
