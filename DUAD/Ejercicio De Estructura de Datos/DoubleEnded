class Node:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


class DoubleEndedQueue:
    def __init__(self):
        self.left = None
        self.right = None

    def push_left(self, value):
        new_node = Node(value)

        if self.left is None:
            self.left = new_node
            self.right = new_node
        else:
            new_node.next = self.left
            self.left.previous = new_node
            self.left = new_node

    def push_right(self, value):
        new_node = Node(value)

        if self.right is None:
            self.left = new_node
            self.right = new_node
        else:
            new_node.previous = self.right
            self.right.next = new_node
            self.right = new_node

    def pop_left(self):
        if self.left is None:
            raise Exception("Queue is empty")

        removed_node = self.left

        if self.left == self.right:
            self.left = None
            self.right = None
        else:
            self.left = self.left.next
            self.left.previous = None

        return removed_node.value

    def pop_right(self):
        if self.right is None:
            raise Exception("Queue is empty")

        removed_node = self.right

        if self.left == self.right:
            self.left = None
            self.right = None
        else:
            self.right = self.right.previous
            self.right.next = None

        return removed_node.value

    def print_queue(self):
        current = self.left

        if current is None:
            print("Queue is empty")
            return

        while current is not None:
            print(current.value)
            current = current.next


queue = DoubleEndedQueue()

queue.push_left(20)
queue.push_left(10)
queue.push_right(30)
queue.push_right(40)

print("Double Ended Queue:")
queue.print_queue()

print("Removed left:", queue.pop_left())
print("Removed right:", queue.pop_right())

print("Queue after pops:")
queue.print_queue()