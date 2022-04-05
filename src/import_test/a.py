"""
__init__ 模块总是最早执行，哪怕是 from mod import sub_mod 也是先执行mod.__init__

>>> 输出结果
load mod/__init__.py
load mod/b.py
"""


from mod import b
