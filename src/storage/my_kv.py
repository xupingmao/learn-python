# -*- coding:utf-8 -*-
"""
@Author       : xupingmao
@email        : 578749341@qq.com
@Date         : 2023-02-01 23:15:02
@LastEditors  : xupingmao
@LastEditTime : 2023-02-05 13:21:29
@FilePath     : /xnoted:/projects/learn-python/src/storage/my_kv.py
@Description  : 键值对存储
"""

import json
import bisect
import threading
import os


class _MemoryDBImpl(object):

    __slots__ = ["_data", "_lock", "_is_snapshot"]

    def __init__(self, data=None, is_snapshot=False):
        if data is None:
            self._data = []
        else:
            self._data = data
        self._lock = threading.RLock()
        self._is_snapshot = is_snapshot

    def close(self):
        with self._lock:
            self._data = []

    def put(self, key, val, **_kwargs):
        if self._is_snapshot:
            raise TypeError("cannot put on leveldb snapshot")
        assert isinstance(key, str)
        assert isinstance(val, str)
        with self._lock:
            idx = bisect.bisect_left(self._data, (key, ""))
            if 0 <= idx < len(self._data) and self._data[idx][0] == key:
                self._data[idx] = (key, val)
            else:
                self._data.insert(idx, (key, val))

    def delete(self, key, **_kwargs):
        if self._is_snapshot:
            raise TypeError("cannot delete on leveldb snapshot")
        with self._lock:
            idx = bisect.bisect_left(self._data, (key, ""))
            if 0 <= idx < len(self._data) and self._data[idx][0] == key:
                del self._data[idx]

    def get(self, key, **_kwargs):
        with self._lock:
            idx = bisect.bisect_left(self._data, (key, ""))
            if 0 <= idx < len(self._data) and self._data[idx][0] == key:
                return self._data[idx][1]
            return None

    # pylint: disable=W0212
    def write(self, batch, **_kwargs):
        if self._is_snapshot:
            raise TypeError("cannot write on leveldb snapshot")
        with self._lock:
            for key, val in batch._puts.iteritems():
                self.put(key, val)
            for key in batch._deletes:
                self.delete(key)

    def iterator(self, **_kwargs):
        # WARNING: huge performance hit.
        # leveldb iterators are actually lightweight snapshots of the data. in
        # real leveldb, an iterator won't change its idea of the full database
        # even if puts or deletes happen while the iterator is in use. to
        # simulate this, there isn't anything simple we can do for now besides
        # just copy the whole thing.
        with self._lock:
            return _IteratorMemImpl(self._data[:])

    def approximateDiskSizes(self, *ranges):
        if self._is_snapshot:
            raise TypeError("cannot calculate disk sizes on leveldb snapshot")
        return [0] * len(ranges)

    def compactRange(self, start_key, end_key):
        pass

    def snapshot(self):
        if self._is_snapshot:
            return self
        with self._lock:
            return _MemoryDBImpl(data=self._data[:], is_snapshot=True)

class StoreFile:
    """db存储，管理1个存储文件"""
    def __init__(self, db_dir="./data", store_file = "./data-1.txt") -> None:
        self.mem_store = _MemoryDBImpl()
        self.last_pos = 0
        self.db_dir = db_dir
        self.store_file = store_file
        self.load_disk()
    
    def load_disk(self):
        fpath = os.path.join(self.db_dir, self.store_file)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        if not os.path.exists(fpath):
            with open(fpath, "w+") as fp:
                pass
        
        with open(fpath, "r+") as fp:
            while True:
                pos = fp.tell()
                line = fp.readline()
                if line.strip() == "":
                    break
                line_data = json.loads(line)
                key = line_data.get("key")
                self.mem_store.put(key, str(pos))
        
        self.write_fp = open(fpath, "a+")
        self.last_pos = self.write_fp.tell()
    
    def write(self, key, val):
        # TODO 优化下编码器，增加校验和删除标记
        self.write_fp.seek(self.last_pos)
        self.write_fp.write(json.dumps(dict(key=key, val=val)))
        self.write_fp.write("\n")
        self.write_fp.flush()
        self.last_pos = self.write_fp.tell()
    
    def close(self):
        self.write_fp.close()
    
    def get(self, key, **kw):
        pos_str = self.mem_store.get(key, **kw)
        if pos_str == None:
            return None
        self.write_fp.seek(int(pos_str))
        line_str = self.write_fp.readline()
        return json.loads(line_str).get("val")
    
    def put(self, key, val, **kw):
        pos = self.write_fp.tell()
        self.mem_store.put(key, str(pos), **kw)
        self.write(key, val)

class MyDB:

    def __init__(self, db_dir = "./data") -> None:
        self.db_dir = db_dir
        self.store = StoreFile(db_dir, "data-1.txt")
    
    def compact(self):
        # TODO 并发控制
        new_store = StoreFile(self.db_dir, "./data-2.txt")
        for key, pos_str in self.store.mem_store._data:
            val = self.get(key)
            if val != None:
                new_store.put(key, val)
        new_store.close()
        # TODO switch data file
    
    def get(self, key):
        return self.store.get(key)
    
    def put(self, key, value):
        return self.store.put(key, value)
    
    def close(self):
        self.store.close()

class Shell:
    
    def __init__(self) -> None:
        self.db = MyDB(db_dir="./test-data")

    def loop(self):
        while True:
            cmd = input(">>> ")
            parts = cmd.split()
            if len(parts) == 0:
                print("bad command")
                continue
            op = parts[0]
            if op == "quit" or op == "exit":
                print("Bye")
                break
            
            attr = "op_" + op
            if hasattr(self, attr):
                meth = getattr(self, attr)
                meth(parts)
            else:
                print("bad command, supported commands: get/put/set")

        self.db.close()
        
    def op_put(self, parts: list[str]):
        if len(parts) != 3:
            print("bad put command")
        else:
            key = parts[1]
            val = parts[2]
            self.db.put(key, val)
            print("OK")
    
    def op_get(self, parts):
        if len(parts) != 2:
            print("bad get command")
        else:
            key = parts[1]
            val = self.db.get(key)
            print(val)
    
    def op_compact(self, parts):
        self.db.compact()
        print("OK")

if __name__ == "__main__":
    shell = Shell()
    shell.loop()
