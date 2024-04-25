# BST Variation 1

from __future__ import annotations
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        : int  = None,
                  value      : int  = None,
                  leftchild  : Node = None,
                  rightchild : Node = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# For the tree rooted at root:
# Return the json.dumps of the list with indent=2.
# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key"        : node.key,
            "value"      : node.value,
            "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# For the tree rooted at root and the key and value given:
# Insert the key/value pair.
# The key is guaranteed to not be in the tree.
def insert(root: Node, key: int, value: int) -> Node:
    
    if root == None:
        return Node(key, value)
    
    curr_node = root
    prev_node = None
    
    new_node = Node(key, value)
    
    while curr_node:
        prev_node = curr_node
        if key < curr_node.key:
            curr_node = curr_node.leftchild
        else:
            curr_node = curr_node.rightchild
    
    if key < prev_node.key:
        prev_node.leftchild = new_node
    else:
        prev_node.rightchild = new_node
        
    return root

# For the tree rooted at root and the key given, delete the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    
    curr_node = root
    prev_node = None
    
    while curr_node.key != key:
        prev_node = curr_node
        if key < curr_node.key:
            curr_node = curr_node.leftchild
        else:
            curr_node = curr_node.rightchild
    
    if curr_node.leftchild == None and curr_node.rightchild == None:
        if prev_node != None:
            if curr_node.key < prev_node.key:
                prev_node.leftchild = None
            else:
                prev_node.rightchild = None
        else:
            return None
    elif curr_node.leftchild == None:
        if prev_node == None:
            return curr_node.rightchild
        else:
            if curr_node.key < prev_node.key:
                prev_node.leftchild = curr_node.rightchild
            else:
                prev_node.rightchild = curr_node.rightchild
            curr_node = None
    elif curr_node.rightchild == None:
        if prev_node == None:
            return curr_node.leftchild
        else: 
            if curr_node.key < prev_node.key:
                prev_node.leftchild = curr_node.leftchild
            else:
                prev_node.rightchild = curr_node.leftchild
            curr_node = None
    else:
        save_delete_node = curr_node
        
        curr_node = curr_node.rightchild
        while curr_node.leftchild != None:
            curr_node = curr_node.leftchild
            
        new_node = Node(curr_node.key, curr_node.value)
        
        new_node.leftchild = save_delete_node.leftchild
        new_node.rightchild = save_delete_node.rightchild
            
        save_delete_node = None
        
        if prev_node != None:
            if new_node.key < prev_node.key:
                prev_node.leftchild = new_node
            else:
                prev_node.rightchild = new_node
        else:
            root = new_node
        
        new_node.rightchild = delete(new_node.rightchild, new_node.key)
        
    return root

# For the tree rooted at root and the key given:
# Calculate the list of values on the path from the root down to and including the search key node.
# The key is guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    # Remove the next line and fill in code to construct value_list.
    value_list = []
    
    curr_node = root
    
    while curr_node.key != search_key:
        value_list.append(curr_node.value)
        if search_key < curr_node.key:
            curr_node = curr_node.leftchild
        else:
            curr_node = curr_node.rightchild
    
    value_list.append(curr_node.value)
    
    return json.dumps(value_list,indent = 2)

def inorder_list(root: Node):
    ret = []

    if root.leftchild:
        ret.extend(inorder_list(root.leftchild))
    ret.append((root.key, root.value))
    if root.rightchild:
        ret.extend(inorder_list(root.rightchild))
    
    return ret

def create_restructure(root: Node, left_list, right_list):
    len_l = len(left_list)
    len_r = len(right_list)
    
    if len_l == 0:
        root.leftchild = None
    elif len_l == 1:
        new_left = Node(left_list[0][0], left_list[0][1])
        root.leftchild = new_left
    else:
        index = len_l // 2
        new_left = Node(left_list[index][0], left_list[index][1])
        root.leftchild = create_restructure(new_left, left_list[:index], left_list[index + 1:])
        
    if len_r == 0:
        root.rightchild = None
    elif len_r == 1:
        new_right = Node(right_list[0][0], right_list[0][1])
        root.rightchild = new_right
    else:
        index = len_r // 2
        new_right = Node(right_list[index][0], right_list[index][1])
        root.rightchild = create_restructure(new_right, right_list[:index], right_list[index + 1:])
    
    return root

# Restructure the tree..
def restructure(root: Node):
    key_value_list = inorder_list(root)
    length = len(key_value_list)
    
    if length == 1:
        return root
    else:
        index = length // 2
        new_root = Node(key_value_list[index][0], key_value_list[index][1])
        create_restructure(new_root, key_value_list[:index], key_value_list[index + 1:])
        
        return new_root