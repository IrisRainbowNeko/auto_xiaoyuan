import pyautogui
import pygetwindow as gw
import numpy as np
import cv2
import win32gui
import win32ui
import win32con
from PIL import Image

class WindowCapture:
    def __init__(self, window_title):
        # 获取窗口
        self.window = gw.getWindowsWithTitle(window_title)[0]

    def capture(self, bbox=(8, 31, 1928, 1111)):
        # 等待窗口响应
        #win32gui.SetForegroundWindow(self.window._hWnd)
        #win32gui.BringWindowToTop(self.window._hWnd)
        #win32gui.ShowWindow(self.window._hWnd, 5)

        x, y, width, height = self.window.left, self.window.top, self.window.width, self.window.height

        # 截取指定窗口区域，包括鼠标
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # 将图片转换成numpy数组，以便后续使用OpenCV处理
        frame = np.array(screenshot)

        # 将RGB转换为BGR，因为OpenCV使用BGR格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if bbox is None:
            return frame
        else:
            return frame[bbox[1]:bbox[3], bbox[0]:bbox[2], ...]

    def get_cursor_icon(self):
        # 获取当前光标信息
        cursor_info = win32gui.GetCursorInfo()
        hcursor = cursor_info[1]
        cursor_pos = cursor_info[2]

        # 创建设备上下文
        hdcScreen = win32gui.GetDC(None)
        hdcScreenObj = win32ui.CreateDCFromHandle(hdcScreen)
        hdcMask = win32ui.CreateDCFromHandle(win32gui.CreateCompatibleDC(hdcScreen))
        hdcColor = win32ui.CreateDCFromHandle(win32gui.CreateCompatibleDC(hdcScreen))

        try:
            bmpColor = win32ui.CreateBitmap()
            bmpMask = win32ui.CreateBitmap()
            bmpColor.CreateCompatibleBitmap(hdcScreenObj, 32, 32)
            bmpMask.CreateCompatibleBitmap(hdcScreenObj, 32, 32)

            hdcMask.SelectObject(bmpMask)
            hdcColor.SelectObject(bmpColor)

            # 绘制光标图标
            win32gui.DrawIconEx(hdcColor.GetSafeHdc(), 0, 0, hcursor, 32, 32, 0, None, win32con.DI_NORMAL)

            # 将位图转换为NumPy数组
            bmp_info = bmpColor.GetInfo()
            bmp_str = bmpColor.GetBitmapBits(True)
            image = np.frombuffer(bmp_str, dtype='uint8')
            image.shape = (bmp_info['bmHeight'], bmp_info['bmWidth'], 4)

            # 转换颜色格式从BGRA到BGR，OpenCV使用BGR
            # image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

            return image
        finally:
            win32gui.ReleaseDC(None, hdcScreen)
            hdcMask.DeleteDC()
            hdcColor.DeleteDC()

if __name__ == '__main__':
    import time
    time.sleep(2)

    # 使用示例
    capture = WindowCapture("雷电模拟器")
    captured_image = capture.capture(bbox=None)

    cv2.imwrite('sc.png', captured_image)

    # 获取光标图标并显示
    #cursor_image = capture.get_cursor_icon()
    #cv2.imwrite('imgs/bull.png', cursor_image)

# Albion Online Client