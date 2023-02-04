
import threading

class Foo:

    def __del__(self):
        print("ThreadName:", threading.currentThread().name)
        raise Exception("del error")


def test_func1():
    f = Foo()
    del f # Exception ignored in: <function Foo.__del__ at 0x7f92483391f0>
    print("after") # 输出 after

def test_func2():
    def inner_func():
        f = Foo()
    inner_func()
    print("after2") # 输出 after2


test_func1()
test_func2()