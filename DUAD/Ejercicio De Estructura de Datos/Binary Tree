class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
        else:
            self._insert_node(self.root, new_node)

    def _insert_node(self, current_node, new_node):
        if new_node.value < current_node.value:
            if current_node.left is None:
                current_node.left = new_node
            else:
                self._insert_node(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
            else:
                self._insert_node(current_node.right, new_node)

    def print_tree(self):
        if self.root is None:
            print("Tree is empty")
        else:
            self._print_in_order(self.root)

    def _print_in_order(self, current_node):
        if current_node is not None:
            self._print_in_order(current_node.left)
            print(current_node.value)
            self._print_in_order(current_node.right)


tree = BinaryTree()

tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)
tree.insert(60)
tree.insert(80)

print("Binary Tree:")
tree.print_tree()