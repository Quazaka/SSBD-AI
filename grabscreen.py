import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2


def setWindowPosition(hwnd):
    win32gui.SetWindowPos(hwnd, 0, 0, 0, 800, 600, 0x0200)


# Get position of window with hwnd
def getScreenPosition():

    hwnd = getHwnd()

    rect = win32gui.GetWindowRect(hwnd)
    return_rect = [rect[0] + 8, rect[1] + 36, rect[2] - 8, rect[3] - 8]

    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (x1:%d, y1:%d, x2:%d, y2:%d)" % (rect[0], rect[1], rect[2], rect[3]))
    print("\tWindow handle: %d" % hwnd)

    return return_rect


# Retrieve the Hammerwatch window handle
def getHwnd():

    hwnd = win32gui.FindWindow(None, "Serious Sam's Bogus Detour - B187")
    # hwnd = win32gui.FindWindow(None, "Gauge")
    # hwnd = win32gui.FindWindow(None, "Hammerwatch 1.32")

    if hwnd == 0:
        hwnd = win32gui.FindWindow(None, "Hammerwatch 1.32 DEBUG")
        if hwnd == 0:
            raise SystemError("Ensure game is running and of correct version")

    return hwnd


# Take a screenshot of window based on window location.
def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    # Instantiate coordinates
    if region:
        x1, y1, x2, y2 = region
        width = x2 - x1 + 1
        height = y2 - y1 + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        x1 = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        y1 = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # Fetch screen from window handle (hwnd) and create bmp
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (x1, y1), win32con.SRCCOPY)

    # Store in buffer and format to usable datatype
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    # Cleanup memory and buffer
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    
    # return image in uniform color scheme
    # return img
    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


# TODO Not sure if needed. Used to convey image to grayscale and highlight edges.
def processImgage(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=300)
    return processed_img


# Display image, debugging only.
def displayImage(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
