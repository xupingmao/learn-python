# -*- coding:utf-8 -*-
# @author mark
# @since 2022/04/17 13:51:11
# @modified 2022/04/17 13:56:53
# @filename iter_finally.py

import traceback

def my_iter():
    try:
        yield 1
        yield 2
        print("my_iter: last")
    finally:
        print("my_iter: finally")


def main1():
    for i in my_iter():
        if i == 1:
            raise Exception("break iter")

def main2():
    for i in my_iter():
        pass

if __name__ == '__main__':
    try:
        main1()
    except:
        traceback.print_exc()

    print("-"*50)
    main2()

r"""输出如下
my_iter: finally
Traceback (most recent call last):
  File "D:\projects\learn-python\src\iter\iter_finally.py", line 29, in <module>
    main1()
  File "D:\projects\learn-python\src\iter\iter_finally.py", line 21, in main1
    raise Exception("break iter")
Exception: break iter
--------------------------------------------------
my_iter: last
my_iter: finally
"""
