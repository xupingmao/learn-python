# -*- coding:utf-8 -*-
# @author xupingmao
# @since 2022/03/23 20:12:04
# @modified 2022/03/24 11:24:16
# @filename bptree_test.py

import time
import random
import sys
from collections import deque

sys.path.append("tools")
from bptree import BpTree

class ArrayMap:
    def __init__(self):
        self.items = []

    def insert(self, key, value):
        for item in self.items:
            if item[0] == key:
                item[1] = value
                return
        self.items.append([key, value])

    def get(self, key):
        for item in self.items:
            if item[0] == key:
                return item[1]
        return None

class TestClass:
    def __init__(self, loops):
        self.loops = loops
        self.print_args = False

    def timeit(self, func, *args):
        t1 = time.time()
        ret = func(*args)
        cost_time = (time.time() - t1) * 1000
        func_name = func.__name__

        if cost_time > 0:
            qps = (self.loops / cost_time * 1000)
        else:
            qps = -1

        if self.print_args:
            args_obj = args
        else:
            args_obj = ""

        print("LOOPS(%d) %s%s cost time:(%.2fms), qps:(%.2f)" % 
            (self.loops, func_name, args_obj, cost_time, qps))
        return ret

def rand_str(length):
    v = ""
    a = ord('A')
    b = ord('Z')
    for i in range(length):
        v += chr(random.randint(a, b))
    return v

def gen_rand_kv_list(size, length = 10):
    result = []
    for i in range(size):
        key = rand_str(length)
        value = rand_str(length)
        result.append((key, value))
    return result

def run_bench_bptree_insert(loops, max_size = 5):
    t = BpTree(None, max_size, True)
    for i in range(loops):
        key = rand_str(10)
        value = rand_str(10)
        t.insert(key, value)
    return t

def run_bench_bptree_insert2(kv_list, max_size = 5):
    t = BpTree(None, max_size, True)
    for key, value in kv_list:
        t.insert(key, value)
    return t

def run_bench_array_insert(loops):
    t = ArrayMap()
    for i in range(loops):
        key = rand_str(10)
        value = rand_str(10)
        t.insert(key, value)
    return t

def run_bench_rand_keyvalue(loops):
    for i in range(loops):
        key = rand_str(10)
        value = rand_str(10)


def run_bench_rand_key(loops):
    for i in range(loops):
        key = rand_str(10)

def run_bench_dict_insert(loops):
    t = dict()
    for i in range(loops):
        key = rand_str(10)
        value = rand_str(10)
        t[key] = value
    return t

def run_bench_dict_insert2(kv_list):
    t = dict()
    for key, value in kv_list:
        t[key] = value
    return t

def run_bench_bptree_get(tree, loops):
    for i in range(loops):
        key = rand_str(10)
        tree.get(key)

def run_bench_array_get(tree, loops):
    return run_bench_bptree_get(tree, loops)

def assert_value(t1, t2, loops):
    for i in range(loops):
        key = rand_str(10)
        v1 = t1.get(key)
        v2 = t2.get(key)
        assert v1 == v2

def run_bench():
    test = TestClass(2000)
    timeit = test.timeit
    test.print_args = False

    kv_list2000 = gen_rand_kv_list(2000)
    kv_list10000 = gen_rand_kv_list(10000)

    timeit(run_bench_dict_insert2, kv_list2000)
    timeit(run_bench_bptree_insert2, kv_list2000, 5)
    print("-" * 50)

    test.loops = 10000
    timeit(run_bench_dict_insert2, kv_list10000)
    timeit(run_bench_bptree_insert2, kv_list10000)
    timeit(run_bench_bptree_insert2, kv_list10000, 5)
    timeit(run_bench_bptree_insert2, kv_list10000, 10)
    timeit(run_bench_bptree_insert2, kv_list10000, 15)
    timeit(run_bench_bptree_insert2, kv_list10000, 20)
    print("-" * 50)

    test.loops = 30000
    timeit(run_bench_rand_keyvalue, 30000)
    timeit(run_bench_dict_insert, 30000)
    timeit(run_bench_bptree_insert, 30000)
    print("-" * 50)

    test.loops = 2000
    t1 = timeit(run_bench_bptree_insert, 2000)
    t1b = timeit(run_bench_bptree_insert, 2000, 10)
    t2 = timeit(run_bench_array_insert, 2000)

    timeit(run_bench_bptree_get, t1, 2000)
    timeit(run_bench_array_get, t2, 2000)

    assert_value(t1, t2, 1000)


def run_test():
    t = BpTree(None, 5, True)
    t.insert_and_print("10")
    t.insert_and_print("20")
    t.insert_and_print("30")
    t.insert_and_print("5")
    t.insert_and_print("6")
    t.insert_and_print("40")
    t.insert_and_print("50")

    for i in range(100):
        t.insert(rand_str(10), None)

    t.print()

def run_test_seq():
    t = BpTree(None, 5, True)

    for i in range(100):
        t.insert(i, None)

    t.print()

def main():
    run_bench()
    # run_test_seq()


if __name__ == '__main__':
    main()
