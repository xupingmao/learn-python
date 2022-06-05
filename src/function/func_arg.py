'''
Author: xupingmao xupingmao@gmail.com
Date: 2022-06-05 14:56:17
LastEditors: xupingmao xupingmao@gmail.com
LastEditTime: 2022-06-05 15:37:53
FilePath: \learn-python\src\function\func_arg.py
Description: 参数的示例，Python的参数有三种
- positional argument
- keyword argument
- any positional arguments
- any keyword arguments
- * 星号禁用 positional argument
'''


def fun1(a, b):
    """普通的位置参数"""
    return "a={a},b={b}".format(a=a, b=b)


def fun2(a, b=1):
    """带默认值的参数, keyword argument"""
    return "a={a},b={b}".format(a=a, b=b)


def fun3(a, b, *args, **kw):
    """声明可变参数和关键字参数"""
    return "a={a},b={b},args={args},kw={kw}".format(a=a, b=b, args=args, kw=kw)


def fun4(*, a = 1, b = 2, **kw):
    """禁止positional argument"""
    return "a={a},b={b},kw={kw}".format(a=a, b=b, kw=kw)


def _assert(a, b):
    assert a == b, "expect: %s\nactual: %s" % (b, a)

# 普通的调用
_assert(fun1(1, 2), "a=1,b=2")

# 不带默认值
_assert(fun2(2), "a=2,b=1")

# 覆盖默认值
_assert(fun2(2, 2), "a=2,b=2")

# 指定参数调用,这时忽略顺序
_assert(fun1(b=1,a=2), "a=2,b=1")

# 传入可选参数
_assert(fun3(1, 2, 3, 4), "a=1,b=2,args=(3, 4),kw={}")

# 传入关键字参数
_assert(fun3(1,2,k1=3,k2=4), "a=1,b=2,args=(),kw={'k1': 3, 'k2': 4}")

# 传入普通参数+关键字 (关键字优先匹配 positional arguments)
_assert(fun3(b=2,a=1,k1=3), "a=1,b=2,args=(),kw={'k1': 3}")

try:
    fun4(1,2)
    assert False, "unexpected reach"
except Exception as e:
    _assert(str(e), "fun4() takes 0 positional arguments but 2 were given")

# 关键字参数
_assert(fun4(b=3,a=1,c=3), "a=1,b=3,kw={'c': 3}")

print("done!")
