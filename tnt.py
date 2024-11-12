import re

class TreeNode:
    def __init__(self, value):
        if not isinstance(value, int) or value < 0 or value >= 100:
            raise ValueError("Node value must be a whole non-negative integer less than 100.")
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class Tree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)

    def add(self, parent_value, child_value):
        try:
            if not isinstance(child_value, int) or child_value < 0 or child_value >= 100:
                raise ValueError("Child value must be a whole non-negative integer less than 100.")
            if child_value == self.root.value:
                raise ValueError("Child value cannot be the same as the root value. Please enter a different value.")

            parent_node = self.find_node(self.root, parent_value)
            if not parent_node:
                raise ValueError(f"Parent node with value {parent_value} not found.")

            if self.find_node(self.root, child_value):
                raise ValueError("Child value already exists in the tree.")

            if child_value < parent_node.value:
                if parent_node.left is None:
                    parent_node.left = TreeNode(child_value)
                    parent_node.left.parent = parent_node
                else:
                    self.add(parent_node.left.value, child_value)
            else:
                if parent_node.right is None:
                    parent_node.right = TreeNode(child_value)
                    parent_node.right.parent = parent_node
                else:
                    self.add(parent_node.right.value, child_value)

            print("Child added successfully.")
            self.display_tree()
        except ValueError as e:
            print(e)

    def find_node(self, current_node, value):
        if current_node is None:
            return None
        if current_node.value == value:
            return current_node
        left_result = self.find_node(current_node.left, value)
        if left_result is not None:
            return left_result
        return self.find_node(current_node.right, value)

    def update(self, old_value, new_value):
        try:
            if not isinstance(new_value, int) or new_value < 0 or new_value >= 100:
                raise ValueError("New value must be a whole non-negative integer less than 100.")

            node_to_update = self.find_node(self.root, old_value)
            if node_to_update is None:
                raise ValueError(f"Node with value {old_value} not found.")

            parent = node_to_update.parent

            if parent:
                if parent.left == node_to_update and new_value >= parent.value:
                    raise ValueError("The new value should be less than the parent.")
                elif parent.right == node_to_update and new_value <= parent.value:
                    raise ValueError("The new value should be greater than the parent.")

            if node_to_update.left and node_to_update.right:
                if not (node_to_update.left.value < new_value < node_to_update.right.value):
                    raise ValueError(
                        "The new value should be greater than the left child and less than the right child.")
            elif node_to_update.left:
                if new_value <= node_to_update.left.value:
                    raise ValueError("The new value should be greater than the left child.")
            elif node_to_update.right:
                if new_value >= node_to_update.right.value:
                    raise ValueError("The new value should be less than the right child.")

            node_to_update.value = new_value
            print("Node updated successfully.")
            self.display_tree()

        except ValueError as e:
            print(e)

    def delete(self, value):
        try:
            if value == self.root.value:
                raise ValueError("Cannot delete the root node.")
            self.root = self._delete_recursive(self.root, value)
            print(f"Node with value {value} deleted.")
            self.display_tree()
        except ValueError as e:
            print(e)

    def _delete_recursive(self, node, value):
        if node is None:
            raise ValueError(f"Node with value {value} not found.")

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with one or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Node with two children, get the in-order successor (smallest in the right subtree)
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def display_tree(self):
        if not self.root:
            print("Tree is empty.")
            return

        lines, *_ = self._display_tree(self.root)
        for line in lines:
            print(line)

    def _display_tree(self, node):
        if node is None:
            return [], 0, 0, 0

        if node.left is None and node.right is None:
            line = '%s' % node.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display_tree(node.left)
            s = '%s' % node.value
            u = len(s)
            first_line = (x + 1) * ' ' + s
            second_line = x * ' ' + '/' + (n - x) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display_tree(node.right)
            s = '%s' % node.value
            u = len(s)
            first_line = s + x * ' ' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display_tree(node.left)
        right, m, q, y = self._display_tree(node.right)
        s = '%s' % node.value
        u = len(s)
        first_line = (x + 1) * ' ' + s + y * ' ' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


    def display_leaf_nodes(self):
        print("\nLeaf Nodes:")
        self._print_leaf_nodes(self.root)

    def _print_leaf_nodes(self, node):
        if node:
            if not node.left and not node.right:
                print(node.value)
            self._print_leaf_nodes(node.left)
            self._print_leaf_nodes(node.right)

    def display_siblings(self):
        print("\nSiblings Grouped:")
        siblings_dict = {}
        self._gather_siblings(self.root, siblings_dict)

        for parent_value, siblings in siblings_dict.items():
            if siblings:
                print(f"Parent {parent_value}: Siblings -> {', '.join(map(str, siblings))}")

    def _gather_siblings(self, node, siblings_dict):
        if node is None:
            return

        # If the node has a parent, we check if the parent is in the dict
        if node.parent:
            if node.parent.value not in siblings_dict:
                siblings_dict[node.parent.value] = []
            siblings_dict[node.parent.value].append(node.value)

        # Traverse the children
        self._gather_siblings(node.left, siblings_dict)
        self._gather_siblings(node.right, siblings_dict)


    def display_root(self):
        print(f"\nRoot Node: {self.root.value}")

    def display_parents(self):
        print("\nParent Nodes:")
        self._print_parents(self.root)

    def _print_parents(self, node):
        if node:
            if node.left or node.right:
                print(node.value)
            self._print_parents(node.left)
            self._print_parents(node.right)

    def display_children(self):
        print("\nChild Nodes:")
        self._print_children(self.root)

    def _print_children(self, node):
        if node:
            if node.left or node.right:
                children = []
                if node.left:
                    children.append(node.left.value)
                if node.right:
                    children.append(node.right.value)
                print(f"Parent {node.value}: Children -> {', '.join(map(str, children))}")
            self._print_children(node.left)
            self._print_children(node.right)


def main():
    print("Binary Tree Command Interface")
    print("Available commands: add <parent> <child>, update <old_value> <new_value>, delete <value>, "
          "display tree, display root, display parents, display children, display leaf nodes, display siblings, exit")

    tree = None
    while True:
        command = input("Enter command: ").strip().lower()
        command_parts = re.split(r'\s+', command)

        if command_parts[0] == 'exit':
            break
        elif command_parts[0] == 'add' and len(command_parts) == 3:
            if tree is None:
                tree = Tree(int(command_parts[1]))
            tree.add(int(command_parts[1]), int(command_parts[2]))
        elif command_parts[0] == 'update' and len(command_parts) == 3:
            if tree is not None:
                tree.update(int(command_parts[1]), int(command_parts[2]))
        elif command_parts[0] == 'delete' and len(command_parts) == 2:
            if tree is not None:
                tree.delete(int(command_parts[1]))
        elif command_parts[0] == 'display':
            if len(command_parts) == 2 and command_parts[1] == 'tree':
                if tree is not None:
                    tree.display_tree()
                else:
                    print("Tree is empty.")
            elif command_parts[1] == 'root':
                if tree is not None:
                    tree.display_root()
                else:
                    print("Tree is empty.")
            elif command_parts[1] == 'parents':
                if tree is not None:
                    tree.display_parents()
                else:
                    print("Tree is empty.")
            elif command_parts[1] == 'children':
                if tree is not None:
                    tree.display_children()
                else:
                    print("Tree is empty.")
            elif command_parts[1] == 'leaf':
                if tree is not None:
                    tree.display_leaf_nodes()
                else:
                    print("Tree is empty.")
            elif command_parts[1] == 'siblings':
                if tree is not None:
                    tree.display_siblings()
                else:
                    print("Tree is empty.")
            else:
                print("Invalid display command.")
        else:
            print("Invalid command.")


if __name__ == '__main__':
    main()
