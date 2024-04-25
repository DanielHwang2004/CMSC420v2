from __future__ import annotations
import json
import math
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key      : int,
                  value    : str,
                  toplevel : int,
                  pointers : List[Node] = None):
        self.key      = key
        self.value    = value
        self.toplevel = toplevel
        self.pointers = pointers

# DO NOT MODIFY!
class SkipList():
    def  __init__(self,
                  maxlevel : int = None,
                  nodecount: int = None,
                  headnode : Node = None,
                  tailnode : Node = None):
        self.maxlevel = maxlevel
        self.nodecount = nodecount
        self.headnode  = headnode
        self.tailnode  = tailnode

    # DO NOT MODIFY!
    # Return a reasonable-looking json.dumps of the object with indent=2.
    # We create an list of nodes,
    # For each node we show the key, the value, and the list of pointers and the key each points to.
    def dump(self) -> str:
        currentNode = self.headnode
        nodeList = []
        while currentNode is not self.tailnode:
            pointerList = str([n.key for n in currentNode.pointers])
            nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
            currentNode = currentNode.pointers[0]
        pointerList = str([None for n in currentNode.pointers])
        nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
        return json.dumps(nodeList,indent = 2)

    # DO NOT MODIFY!
    # Creates a pretty rendition of a skip list.
    # It's vertical rather than horizontal in order to manage different lengths more gracefully.
    # This will never be part of a test but you can put "pretty" as a single line in your tracefile
    # to see what the result looks like.
    def pretty(self) -> str:
        currentNode = self.headnode
        longest = 0
        while currentNode != None:
            if len(str(currentNode.key)) > longest:
                longest = len(str(currentNode.key))
            currentNode = currentNode.pointers[0]
        longest = longest + 2
        pretty = ''
        currentNode = self.headnode
        while currentNode != None:
            lineT = 'Key = ' + str(currentNode.key) + ', Value = ' + str(currentNode.value)
            lineB = ''
            for p in currentNode.pointers:
                if p is not None:
                    lineB = lineB + ('('+str(p.key)+')').ljust(longest)
                else:
                    lineB = lineB + ''.ljust(longest)
            pretty = pretty + lineT
            if currentNode != self.tailnode:
                pretty = pretty + "\n"
                pretty = pretty + lineB + "\n"
                pretty = pretty + "\n"
            currentNode = currentNode.pointers[0]
        return(pretty)
    
    def print_skip_list(self):
        # Customization
        spacer_length, decimal_place = 4, 4
        h_char, v_char, arrow_head = "-", "|", ">"

        # Helper String
        spacer = h_char * spacer_length
        empty_spacer = " " * spacer_length
        arrow = h_char * (spacer_length - 1) + arrow_head
        delimiter = v_char + h_char * decimal_place + v_char

        # Head node to string
        lines = [""] * (self.maxlevel + 3)
        for i in range(self.maxlevel + 1):
            lines[i + 2] = v_char + f"{self.headnode.pointers[i].key:>{decimal_place}}" + v_char
        lines[1] += delimiter
        lines[0] += v_char + f'{self.headnode.key:>{decimal_place}}' + v_char

        # Rest of the nodes to string
        current_node = self.headnode.pointers[0]
        while current_node is not None:
            # Iterate through each pointer
            for i in range(self.maxlevel + 1):
                if i < len(current_node.pointers):
                    # Node levels with pointers
                    pointer = current_node.pointers[i]
                    pointer_key = pointer.key if pointer else str(pointer)  # Edge case for tail node
                    lines[i + 2] += arrow + v_char + f"{pointer_key:>{decimal_place}}" + v_char
                else:
                    # Node levels with no pointers
                    lines[i + 2] += spacer + h_char * (decimal_place + 2)
            # Reserve bottom two lines for this node's key
            lines[1] += empty_spacer + delimiter
            lines[0] += empty_spacer + v_char + f'{current_node.key:>{decimal_place}}' + v_char
            current_node = current_node.pointers[0]

        # Print Results
        for line in reversed(lines):
            print(line)

        print("")

    # DO NOT MODIFY!
    # Initialize a skip list.
    # This constructs the headnode and tailnode each with maximum level maxlevel.
    # Headnode has key -inf, and pointers point to tailnode.
    # Tailnode has key inf, and pointers point to None.
    # Both have value None.
    def initialize(self,maxlevel):
        pointers = [None] * (1+maxlevel)
        tailnode = Node(key = float('inf'),value = None,toplevel = maxlevel,pointers = pointers)
        pointers = [tailnode] * (maxlevel+1)
        headnode = Node(key = float('-inf'),value = None, toplevel = maxlevel,pointers = pointers)
        self.headnode = headnode
        self.tailnode = tailnode
        self.maxlevel = maxlevel

    # Create and insert a node with the given key, value, and toplevel.
    # The key is guaranteed to not be in the skiplist.
    # Check if we need to rebuild and do so if needed.
    def insert(self,key,value,toplevel):
        
        if not self.nodecount:
            self.nodecount = 0
            
        self.nodecount += 1
        
        if math.log2(self.nodecount) + 1 > self.maxlevel:
            
            self.maxlevel = self.maxlevel * 2
            
            key_value_list = []
            
            curr = self.headnode.pointers[0]
            while curr.key < key:
                key_value_list.append((curr.key, curr.value))
                curr = curr.pointers[0]
            
            key_value_list.append((key, value))
            
            while curr.key < float('inf'):
                key_value_list.append((curr.key, curr.value))
                curr = curr.pointers[0]
            
            self.initialize(self.maxlevel)
            self.nodecount = 0
            
            for i, (key, value) in enumerate(key_value_list):
                level_check = i + 1
                level = 0
                
                while (level_check % 2 == 0) and level < self.maxlevel:
                    level += 1
                    level_check /= 2
                
                self.insert(key, value, level)
                
        else:
            add = Node(key, value, toplevel, [])
            
            pointer_list = [None] * (toplevel + 1)
            
            curr = self.headnode
            
            while curr.key < key:
                
                for i in range(len(curr.pointers)):
                    if i < toplevel + 1:
                        pointer_list[i] = curr
                    else:
                        break
                    
                curr = curr.pointers[0]
            
            for i, pointer in enumerate(pointer_list):
                save = pointer.pointers[i]
                
                pointer.pointers[i] = add
                
                add.pointers.append(save)


    # Delete node with the given key.
    # The key is guaranteed to be in the skiplist.
    def delete(self,key):
        print('Placeholder')

    # Search for the given key.
    # Construct a list of all the keys in all the nodes visited during the search.
    # Append the value associated to the given key to this list.
    def search(self,key) -> str:
        A = ['your list gets constructed here']
        return json.dumps(A,indent = 2)