# encoding=utf-8
import multiprocessing
import time


def f(i, ):
    print("i:", i)
    time.sleep(5)


if __name__ == "__main__":
    for i in range(10):
        p = multiprocessing.Process(target=f, args=(i, ))
        p.start()

