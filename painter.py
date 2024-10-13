from controller import MouseController


class Painter:
    def __init__(self, sx, sy, fast=False):
        self.mouse_ctrl = MouseController(sx + 140, sy + 850)
        self.fast = fast
        self.num_path = {
            '.': [(40, 80), (40, 80)],
            '-': [(20, 50), (60, 50)],
            '0': [(40, 0), (0, 30), (0, 70), (40, 100), (80, 70), (80, 30), (40, 0)],
            '1': [(40, 0), (40, 100)],
            '2': [(0, 30), (40, 0), (80, 30), (0, 100), (80, 100)],
            '3': [(0, 25), (40, 0), (80, 25), (30, 50), (80, 75), (40, 100), (0, 75)],
            '4': [(80, 50), (0, 50), (40, 0), (40, 100)],
            '5': [(80, 0), (0, 0), (0, 40), (80, 70), (0, 100)],
            '6': [(40, 0), (0, 50), (40, 100), (80, 50), (0, 50)],
            '7': [(0, 0), (80, 0), (40, 100)],
            '8': [(40, 0), (0, 25), (80, 75), (40, 100), (0, 75), (80, 25), (40, 0)],
            '9': [(40, 100), (80, 50), (40, 0), (0, 50), (80, 50)],

            '>': [(0,0), (80, 50), (0, 100)],
            '<': [(80,0), (0, 50), (80, 100)],
            '=': [(0,0), (50, 0), (50, 0, 50, 50), (0, 50)],
        }

    def paint(self, num_str: str, ofx=0, ofy=0):
        if num_str.endswith('.0'):
            num_str = num_str[:-2]
        for i, ch in enumerate(num_str):
            path = self.num_path[ch]

            self.mouse_ctrl.down((path[0][0] + 100 * i + ofx, path[0][1] + ofy))
            for pos in path[1:]:
                if len(pos)==4:
                    self.mouse_ctrl.up((pos[0] + 100 * i + ofx, pos[1] + ofy))
                    self.mouse_ctrl.down((pos[2] + 100 * i + ofx, pos[3] + ofy))
                else:
                    if self.fast:
                        self.mouse_ctrl.move_to_fast(pos[0] + 100 * i + ofx, pos[1] + ofy)
                    else:
                        self.mouse_ctrl.move_to(pos[0] + 100 * i + ofx, pos[1] + ofy, speed=10)
            self.mouse_ctrl.up((path[-1][0] + 100 * i + ofx, path[-1][1] + ofy))

    def paint_frac(self, num_str: str):
        try:
            up, down = num_str.split('/')
            self.paint(up)
            self.mouse_ctrl.down((0, 120))
            self.mouse_ctrl.move_to(200, 120, speed=50)
            self.mouse_ctrl.up((200, 120))
            self.paint(down, ofy=140)
        except:
            self.paint(num_str)

if __name__ == '__main__':
    from capture import WindowCapture

    capture = WindowCapture("雷电模拟器")

    painter = Painter(capture.window.left, capture.window.top)

    painter.paint('12')
