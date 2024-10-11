import re
from itertools import cycle

import cv2
from PIL import Image
from pix2text import Pix2Text
from sympy import symbols, Eq, solve, sympify


class MathSolver:
    def __init__(self):
        self.latex_model = Pix2Text.from_config(device='cuda', enable_table=False)
        self.allowlist = '0123456789()-+=x?.'
        self.z = symbols('z')

    def replace_sym(self, str_ref, str_src):
        syms = (c for c in str_ref if c in '+/')
        symbol_iter = cycle(syms)
        result = ''.join(next(symbol_iter) if c == '+' else c for c in str_src)
        return result

    def recognize(self, img):
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        tex = self.latex_model.recognize_text_formula(img_pil, return_text=True)
        print('Latex识别结果:', tex)
        tex = re.sub(r'\\ref{[^{}]+}', r'?', tex)
        text = tex.replace(r'\quad', '').replace(' ', '').replace(r'\div', '/').replace(r'\times', '*').replace('$', '').replace('x','*')

        pattern = r'\\frac{([^{}]+)}{([^{}]+)}'
        text = re.sub(pattern, r'(\1)/(\2)', text)

        text = re.sub(r'[^0-9()+\-*/=?.]', '', text).strip().replace('?', 'z')
        return text

    def solve(self, text):
        # 将字符串解析为方程
        lhs, rhs = text.split('=')
        if len(lhs)==0:
            lhs='z'
        if len(rhs)==0:
            rhs='z'

        equation = Eq(sympify(lhs), sympify(rhs))
        solution = solve(equation, self.z)[0]
        return solution

    def solve_bigger(self, left, right):
        left = eval(left)
        right = eval(right)
        if left>right:
            return '>'
        elif left==right:
            return '='
        else:
            return '<'


if __name__ == '__main__':
    solver = MathSolver()
    img = cv2.imread('sc.png')[390:560, 70:660, :]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

    cv2.imwrite('tt.png', img)
    #img = cv2.imread('tt.png')
    text = solver.recognize(img)
    print(text)
    solution = solver.solve(text)
    print(type(solution))
    print(str(solution))

