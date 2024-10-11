import win32api, win32con
import time
import math

import ctypes

awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)

MOUSE_LEFT = 0
MOUSE_MID = 1
MOUSE_RIGHT = 2
mouse_list_down = [win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_RIGHTDOWN]
mouse_list_up = [win32con.MOUSEEVENTF_LEFTUP, win32con.MOUSEEVENTF_MIDDLEUP, win32con.MOUSEEVENTF_RIGHTUP]

from win32api import GetSystemMetrics

print("Screen Width =", GetSystemMetrics(0))
print("Screen Height =", GetSystemMetrics(1))


def mouse_down(x, y, button=MOUSE_LEFT):
    time.sleep(0.02)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(mouse_list_down[button], 0, 0, 0, 0)


def mouse_move(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)


def move_mouse_to(to_x, to_y, speed=10):
    from_x, from_y = win32api.GetCursorPos()
    distance = math.sqrt((to_x - from_x) ** 2 + (to_y - from_y) ** 2)
    steps = int(distance / speed)

    if steps == 0:
        return

    x_step = (to_x - from_x) / steps
    y_step = (to_y - from_y) / steps

    current_x, current_y = from_x, from_y

    for i in range(steps):
        current_x += x_step
        current_y += y_step
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(current_x - from_x), int(current_y - from_y), 0, 0)
        from_x, from_y = int(current_x), int(current_y)  # 更新当前的整数位置
        time.sleep(0.005)  # 控制鼠标移动速度

    # 确保鼠标准确到达指定位置
    win32api.SetCursorPos((to_x, to_y))

def mouse_up(x, y, button=MOUSE_LEFT):
    time.sleep(0.02)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(mouse_list_up[button], 0, 0, 0, 0)

def mouse_to(x, y):
    win32api.SetCursorPos((x, y))

def mouse_click(x, y, button=MOUSE_LEFT):
    mouse_down(x, y, button)
    mouse_up(x, y, button)

def scroll(delta):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta)

def release_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def press_key(key_code):
    win32api.keybd_event(key_code, win32api.MapVirtualKey(key_code, 0), 0, 0)


def tap_key(key_code, t):
    press_key(key_code)
    time.sleep(t)
    release_key(key_code)


class MouseController:
    def __init__(self, sx, sy):
        self.ofx = sx
        self.ofy = sy

    def set_offset(self, ofx, ofy):
        self.ofx = ofx
        self.ofy = ofy

    def move(self, dx, dy):
        mouse_move(dx + self.ofx, dy + self.ofy)

    def move_steps(self, dx, dy, n=10, t=1):
        idx = dx / n
        idy = dy / n
        dt = t / n

        for i in range(n):
            self.move(int(idx), int(idy))
            time.sleep(dt)

    def move_to(self, x, y, speed=10):
        move_mouse_to(x + self.ofx, y + self.ofy, speed)

    def down(self, pos, button=MOUSE_RIGHT):
        mouse_down(pos[0] + self.ofx, pos[1] + self.ofy, button)

    def up(self, pos, button=MOUSE_RIGHT):
        mouse_up(pos[0] + self.ofx, pos[1] + self.ofy, button)

    def to(self, x, y):
        mouse_to(x + self.ofx, y + self.ofy)

    def scroll(self, delta, step=1):
        for i in range(delta//step):
            scroll(step)
            time.sleep(0.02)

    def click(self, pos, t=0.1, button=MOUSE_RIGHT):
        self.down(pos, button=button)
        time.sleep(t)
        self.up(pos, button=button)

    def tap_key(self, key_code, t):
        tap_key(key_code, t)

if __name__ == '__main__':
    import time
    time.sleep(1)

    contollor = MouseController(0, 0)
    contollor.move_to(500, 500)