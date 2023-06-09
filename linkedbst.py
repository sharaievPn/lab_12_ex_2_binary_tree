"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
from time import time
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            res = ""
            if node != None:
                res += recurse(node.right, level + 1)
                res += "| " * level
                res += str(node.data) + "\n"
                res += recurse(node.left, level + 1)
            return res

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    def find_while(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        current = self._root
        while current is not None:
            if item == current.data:
                return current
            elif item < current.data:
                current = current.left
            else:
                current = current.right

        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def add_while(self, item):
        """Adds item to the tree."""

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1

        # Helper function to search for item's position
        current = self._root
        while True:
            # New item is less, go left until spot is found
            if item < current.data:
                if current.left is None:
                    current.left = BSTNode(item)
                    self._size += 1
                    break
                else:
                    current = current.left
            # New item is greater or equal, go right until spot is found
            else:
                if current.right is None:
                    current.right = BSTNode(item)
                    self._size += 1
                    break
                else:
                    current = current.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(c) for c in [top.left, top.right])

        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        nodes_num = self._size
        if height == 0:
            return False
        return height < 2 * log(nodes_num + 1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        nodes = [item for item in list(self.inorder())]
        if low not in nodes or high not in nodes:
            return []

        return nodes[nodes.index(low):nodes.index(high) + 1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = sorted([item for item in list(self.inorder())])
        self.clear()

        def builder(lst):
            if len(lst) == 0:
                return None
            if len(lst) == 1:
                return BSTNode(lst[0])
            position = len(lst) // 2
            root = BSTNode(lst[position])
            root.left = builder(lst[:position])
            root.right = builder(lst[position + 1:])
            self._size += 1
            return root

        self._root = builder(nodes)

        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self.height() == 0:
            return None
        nodes = sorted([item for item in list(self.inorder())])
        if item not in nodes:
            return nodes[-1]
        try:
            return nodes[nodes.index(item) + 1]
        except IndexError:
            return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        if self.height() == 0:
            return None
        nodes = sorted([item for item in list(self.inorder())])
        if item not in nodes:
            return None
        try:
            if nodes.index(item) - 1 == -1:
                return None
            return nodes[nodes.index(item) - 1]
        except IndexError:
            return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r') as file:
            content = file.read().strip()
            content = list(sorted(content.split()))
            file.close()

        new_content = content + []
        random.shuffle(new_content)
        new_content = new_content[:10000]

        def sorted_list_tree():
            print('Started creating sorted tree list')
            self.clear()
            for word in content:
                self.add_while(word)
            print('List created')

        def unordered_tree_dictionary(lst):
            random.shuffle(lst)
            print('Started creating unordered dictionary tree')
            self.clear()
            for word in lst:
                self.add_while(word)
            print('Unordered dictionary list created')

        def find_in_unordered_list_tree():
            print('Started looking up in unordered tree dictionary')
            start_time = time()
            for word in new_content:
                self.find_while(word)
            result_time = time() - start_time
            return f"Search of 10000 random words using unordered tree dictionary " \
                   f"is {round(result_time, 3)} seconds."

        def find_in_sorted_list_tree():
            print('Started looking up in sorted tree dictionary')
            start_time = time()
            for word in new_content:
                self.find_while(word)
            result_time = time() - start_time
            return f"Search of 10000 random words using sorted tree dictionary " \
                   f"is {round(result_time, 3)} seconds."

        def search_in_list():
            print('Searching in list')
            start_time = time()
            for word in new_content:
                content.index(word)
            result_time = time() - start_time
            return f"Search of 10000 random words using list " \
                   f"is {round(result_time, 3)} seconds."

        def balance_tree():
            print('Started tree balancing')
            self.rebalance()
            print('Balancing ended')

        def lookup_in_rebalanced():
            print('Started looking up in balanced tree')
            start_time = time()
            for word in new_content:
                self.find_while(word)
            result_time = time() - start_time
            return f"Search of 10000 random words using balanced tree dictionary " \
                   f"is {round(result_time, 3)} seconds."

        print(search_in_list())
        print()
        sorted_list_tree()
        print()
        print(find_in_sorted_list_tree())
        print()
        unordered_tree_dictionary(content)
        print()
        print(find_in_unordered_list_tree())
        balance_tree()
        print()
        print(lookup_in_rebalanced())
        print()
        balance_tree()
        print()
        print(lookup_in_rebalanced())


tree = LinkedBST()
# print(tree)
# # print(tree._root.data)
# tree.rebalance()
# print(tree)
# print(tree._root.right.data)
# print(tree.predecessor())
# print(tree.rebalance())
# print(tree)
# tree.rebalance()
# print(tree)
# print(tree.rangeFind(10, 1))
# print(tree.demo_bst('words.txt'))
for i in range(10):
    tree.add(i)
print(tree)
tree.rebalance()
print(tree)
