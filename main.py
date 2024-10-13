import time

import argparse
import cv2
from sympy import Integer, Float, Rational

from capture import WindowCapture
from painter import Painter
from solver import MathSolver

import psutil
p = psutil.Process()
p.nice(psutil.REALTIME_PRIORITY_CLASS)


def convert_to_python_type(sympy_number):
    if isinstance(sympy_number, Integer):
        return int(sympy_number)
    elif isinstance(sympy_number, Float):
        return float(sympy_number)
    elif isinstance(sympy_number, Rational):
        return float(sympy_number)
    else:
        raise TypeError("Unsupported type")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='agent argument')
    parser.add_argument('--fast', action='store_true', default=False, help='更快的画结果，但电脑性能不足会不稳定')
    args = parser.parse_args()

    capture = WindowCapture("雷电模拟器")
    solver = MathSolver()
    painter = Painter(capture.window.left, capture.window.top, fast=args.fast)

    while True:
        mode = int(input('选择模式:'))
        for i in range(20):
            for t in range(3):
                try:
                    #img = capture.capture(bbox=[50, 432, 700, 526])
                    img = capture.capture(bbox=[50, 390, 700, 560])
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

                    if mode==0: #算数模式
                        text = solver.recognize(img)
                        print('化简结果:', text)
                        solution = solver.solve(text)
                        if isinstance(solution, Rational):
                            print('解答:', solution)
                            painter.paint_frac(str(solution))
                        else:
                            solution = convert_to_python_type(solution)
                            solution = str(round(solution, 5))
                            print('解答:', solution)

                            painter.paint(solution)
                    else: #比大小模式
                        text_l = solver.recognize(img[:,:260])
                        text_r = solver.recognize(img[:,400:])
                        print('化简结果:', text_l, text_r)

                        solution = solver.solve_bigger(text_l, text_r)
                        print('解答:', solution)
                        painter.paint(solution)

                    time.sleep(0.4)
                    break
                except Exception as e:
                    print(e)