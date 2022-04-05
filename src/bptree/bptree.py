# -*- coding:utf-8 -*-
# @author xupingmao
# @since 2022/03/23 09:06:17
# @modified 2022/03/23 21:30:31
# @filename bptree.py


"""B+树的实现
对于一个非叶子节点A，它有n个子节点，每个节点的值是V(n)，满足下面2个条件
1. 当 0 <= i <= n-1 时满足 Max(第i个值的子节点) <= V(i)
2. 当 i = n 时满足 Max(第i个值的子节点值) > V(i)
"""

class BpTree:

    PAGENO = 0 # 页号

    def __init__(self, parent, max_size, is_leaf):
        assert max_size >= 2
        self.is_leaf = is_leaf
        self.nodes  = []     # 非叶子节点专用
        self.values = []     # 叶子节点专用
        self.parent = parent # 父级节点
        self.max_size = max_size # 每个节点的最大子节点数量
        self.max_key = None # 如果是每层最后一个节点,max_key不准确
        self.pageno  = BpTree.PAGENO
        
        BpTree.PAGENO += 1


    def get(self, key):
        if self.is_leaf:
            return self.get_by_leaf(key)

        assert len(self.nodes) > 0

        for node in self.nodes:
            if key <= node.max_key:
                return node.get(key)

    def get_by_leaf(self, key):
        # TODO 这里可以优化成二分查找
        for item in self.values:
            if item[0] == key:
                return item[1]
        return None

    def insert(self, key, value):
        if self.is_leaf:
            return self.insert_to_leaf(key, value)

        assert len(self.nodes) > 0

        for node in self.nodes:
            if key <= node.max_key:
                return node.insert(key, value)

        # 如果大于或者等于这些子树的值都放到最后一个节点
        return self.nodes[-1].insert(key, value)


    def insert_to_leaf(self, key, value):
        # TODO：可以使用二分法查找
        for item in self.values:
            if item[0] == key:
                item[1] = value
                return

        self.values.append([key, value])
        self.values.sort(key = lambda x:x[0])

        self.max_key = self.values[-1][0]
        
        if len(self.values) > self.max_size:
            self.split()

    def set_values(self, values):
        self.is_leaf = True
        self.values = values
        self.nodes = None
        self.max_key = values[-1][0]

    def set_nodes(self, nodes):
        self.is_leaf = False
        self.values = None
        self.nodes = nodes
        self.max_key = nodes[-1].max_key
        for node in nodes:
            node.parent = self

    def split(self):
        if self.is_leaf:
            mid = len(self.values) // 2
            left_values = self.values[:mid]
            right_values = self.values[mid:]
            
            left_tree  = BpTree(None, self.max_size, True)
            left_tree.set_values(left_values)

            right_tree = BpTree(None, self.max_size, True)
            right_tree.set_values(right_values)
        else:
            mid = len(self.nodes) // 2
            left_nodes = self.nodes[:mid]
            right_nodes = self.nodes[mid:]
            
            left_tree = BpTree(None, self.max_size, False)
            left_tree.set_nodes(left_nodes)

            right_tree = BpTree(None, self.max_size, False)
            right_tree.set_nodes(right_nodes)


        if self.parent is None:
            # 跟节点，插入到自己的子节点中
            self.is_leaf = False
            self.values = None
            self.nodes = []
            self.insert_tree(left_tree)
            self.insert_tree(right_tree)
            assert len(self.nodes) == 2 # 这里是不会再发生split的
            self.max_key = None
            self.height = None
        else:
            # 非根节点，往父级节点插入
            self.parent.delete_tree(self)
            self.parent.insert_tree(left_tree)
            self.parent.insert_tree(right_tree)
            self.parent.check_and_split()

    def delete_tree(self, tree):
        # 子节点的parent处理
        self.nodes.remove(tree)

    def insert_tree(self, tree):
        tree.parent = self
        self.nodes.append(tree)
        self.nodes.sort(key = lambda x:x.max_key)

    def check_and_split(self):
        if len(self.nodes) > self.max_size:
            self.split()

    def calc_height(self):
        if self.parent == None:
            return 1
        else:
            return 1 + self.parent.calc_height()

    def parent_id(self):
        if self.parent != None:
            return str(self.parent.pageno)
        else:
            return "NULL"

    def to_str(self):
        indent = (self.calc_height()-1) * 2
        indent_str = " " * indent

        result = []
        result.append(indent_str)
        result.append("page(%s)" % self.pageno)
        if self.is_leaf:
            result.append(",<叶子节点>")
            result.append(",values(%s)" % self.values)
        else:
            nodes_values = [x.max_key for x in self.nodes]
            result.append(",nodes(%s)" % nodes_values)

        result.append(",parent(%s)" % self.parent_id())

        return "".join(result)


    def print(self):
        print(self.to_str())
        if not self.is_leaf:
            for node in self.nodes:
                node.print()


    def insert_and_print(self, key, value = None):
        self.insert(key, value)
        print("insert(%s,%s)" % (key, value))
        self.print()
        print("")
