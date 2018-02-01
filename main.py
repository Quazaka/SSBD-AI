import grabscreen as gs
from utility import testMovement, countdown
import time
from directkeys import PressKey, ReleaseKey, W

def main():

    # Start countdown so you have time to make Hammerwatch the active windowwd
    countdown(3)

    # gs.setWindowPosition(gs.getHwnd())

    # Get Hammerwatch window position
    pos = gs.getScreenPosition()

    # Collect frame for x frames. True is a valid input for infinite loop.
    collectScreenInThread(pos, 50)

    # Test basic movement

    PressKey(W)
    ReleaseKey(W)

    # testMovement()




# Loop that keeps and stores 10 frames from the game.
def collectScreenInThread(pos, x):
    print("Thread saving frames from game.")
    i = 0
    while i < x:
        screen = gs.grab_screen(region=pos)
        state = []
        state.insert(0, screen)

        # Ensure we only keep the last 10 frames (1 sec) in memory.
        if len(state) == 10:
            state.pop()

        processed_screen = gs.processImgage(screen)
        gs.displayImage(processed_screen)  # TODO Debug
        time.sleep(0.1)  # 10 fps.
        i += 1


if __name__ == "__main__":
    main()
