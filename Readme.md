# 介绍
本项目使用能够识别公式为Latex代码的OCR AI实现自动化小猿口算。没有任何抓包或逆向相关的操作，非侵入式纯视觉算法实现。
安全可靠，泛化性强。

项目仅供学习交流，不回答小白问题。要有pytorch编程基础。

# 使用
安装[pytorch](https://pytorch.org/)和[c++编译环境](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)

安装依赖
```bash
pip install -r requirements.txt
```

运行程序(管理员权限启动):
```bash
python main.py
```

模式0是计算模式，模式1是比大小模式