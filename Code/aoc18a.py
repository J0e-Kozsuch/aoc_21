import ast
import math

file = open(r'C:\Users\16099\Documents\AOC_21\aoc18_snailfish_sums.txt')
by = file.read()

text_lines = by.split("\n")

list_lines = [ast.literal_eval(line) for line in text_lines]

         

    


class number_leaf:

    def __init__(self, parent, value, level, left):

        self._parent = parent
        self.value = value
        self.level = level
        self.left = left

    def return_value(self):
        return self.value

    def get_parent(self):
        return self._parent


class list_node:

    def __init__(self, elements, level = 0, left = None, parent = None):

        self._elements = elements
        self._parent = parent
        self._children = {}
        self.level = level
        self.left = left

    def return_value(self):
        return [self._children['left'].return_value(), self._children['right'].return_value()] 


    def set_parent(self, parent):
        self._parent = parent

    def set_children(self, left_node, right_node):
        self._children['left'] = left_node
        self._children['right'] = right_node

    def get_parent(self):
        return self._parent

    def get_children(self):
        return self._children

    def create_children_nodes(self):

        if type(self._elements[0]) == int:
            self._children['left'] = number_leaf(self, self._elements[0], self.level + 1, True)
        else:
            child = list_node(self._elements[0], self.level + 1, True, self)
            child.create_children_nodes()
            self._children['left'] = child
            
        if type(self._elements[1]) == int:
            self._children['right'] = number_leaf(self, self._elements[1], self.level + 1, False)
            
        else:
            child = list_node(self._elements[1], self.level + 1, False, self)
            child.create_children_nodes()
            self._children['right'] = child

    
    def calculate_magnitude(self):

        if type(self._children['left']) == list_node:
            left_element = self._children['left'].calculate_magnitude()
        else:
            left_element = self._children['left'].value
        left_element *= 3

        if type(self._children['right']) == list_node:
            right_element = self._children['right'].calculate_magnitude()
        else:
            right_element = self._children['right'].value
        right_element *= 2

        return left_element + right_element


            
def find_explode(root):
    children = root.get_children()

    if type(children['left']) == list_node and children['left'].level >= 4:
        child_pair = children['left'].get_children()
        if type(child_pair['left']) == number_leaf and type(child_pair['right']) == number_leaf:
            return children['left']
        else:
            find_explode(children['left'])

    if type(children['left']) == list_node:
        explode_node = find_explode(children['left'])
        if explode_node:
            return explode_node

    if type(children['right']) == list_node and children['right'].level >= 4:
        child_pair = children['right'].get_children()
        if type(child_pair['left']) == number_leaf and type(child_pair['right']) == number_leaf:
            return children['right']
        else:
            find_explode(children['right'])

    if type(children['right']) == list_node:
        explode_node = find_explode(children['right'])
        if explode_node:
            return explode_node

    return False


def explode_left_node(explode_node):
    node = explode_node

    is_left = node.left

    if is_left:

        while node.level != 0 and is_left:
            node = node.get_parent()
            previous_node_left = is_left
            is_left = node.left

        if node.level == 0 and previous_node_left:
            # if travels to top node from left side
            return None
 
    node = node.get_parent()
    node = node.get_children()['left']

    
    while type(node) == list_node:
        node = node.get_children()['right']

    node.value += explode_node.get_children()['left'].value


def explode_right_node(explode_node):
    node = explode_node

    is_right = not node.left

    if is_right:

        while node.level != 0 and is_right:
            node = node.get_parent()
            previous_node_right = is_right
            is_right = not node.left

        if node.level == 0 and previous_node_right:
            # if travels to top node from right side
            return None

    node = node.get_parent()
    node = node.get_children()['right']
    
    while type(node) == list_node:
        node = node.get_children()['left']

    node.value += explode_node.get_children()['right'].value 
            

def check_and_process_explode(root):
   
    explode_node = find_explode(root)

    if not explode_node:
        return False

    children = explode_node.get_children()

    right_value = children['right'].value

    # add left value to first left leaf
    explode_left_node(explode_node)

    # add right value to first right leaf
    explode_right_node(explode_node)
    
    # replace explode list node with number leaf of 0
    parent_node = explode_node.get_parent()

    is_left = explode_node.left

    if is_left:
        parent_right_child = parent_node.get_children()['right']
        parent_node.set_children(number_leaf(parent = parent_node, value = 0, level = parent_right_child.level, left = True), parent_right_child)
    else:
        parent_left_child = parent_node.get_children()['left']
        parent_node.set_children(parent_left_child, number_leaf(parent = parent_node, value = 0, level = parent_left_child.level, left = False))

    return True
        
                                    

def find_split(root):
    node = root
    
    while True:
        if type(node) == number_leaf and node.left:
            if node.value > 9:
                return node
            node = node.get_parent()
            node = node.get_children()['right']

        elif type(node) == number_leaf and not node.left:
            if node.value > 9:
                return node

            while not node.left and node.level > 0:
                node = node.get_parent()
            if node.level == 0:
                return False
            
            node = node.get_parent()
            
            node = node.get_children()['right']

        else:
            while type(node) == list_node:
                node = node.get_children()['left']

            
def check_and_process_split(root):
    split_node = find_split(root)

    if not split_node:
        return False

    split_node_is_left = split_node.left
    split_node_level = split_node.level
    left_value = int(math.floor(split_node.value / 2))
    right_value = int(math.ceil(split_node.value / 2))

    parent_node = split_node.get_parent()

    new_node = list_node([left_value, right_value], split_node_level, split_node_is_left, parent_node)
    new_node.create_children_nodes()    

    if split_node_is_left:
        parent_right_child = parent_node.get_children()['right']
        parent_node.set_children(new_node, parent_right_child)
    else:
        parent_left_child = parent_node.get_children()['left']
        parent_node.set_children(parent_left_child, new_node)

    return True

    
        
    

def reduce(tree):

    # set to true to define and to allow while loop to start
    exploded = True
    split = True

    while exploded or split:
        
        exploded = check_and_process_explode(tree)

        if exploded:
            continue

        split = check_and_process_split(tree)

def add_numbers(tree1, tree2):

    new_tree = list_node([tree1.return_value(),tree2.return_value()], 0, None, None)

    new_tree.create_children_nodes()

    return new_tree

## add up results

master_tree = list_node(list_lines[0], 0, None, None)

master_tree.create_children_nodes()

for number in list_lines[1:]:
    tree = list_node(number, 0, None, None)

    tree.create_children_nodes()

    master_tree = add_numbers(master_tree, tree)

    reduce(master_tree)
    


print(master_tree.calculate_magnitude())




