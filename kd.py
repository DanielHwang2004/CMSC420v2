from __future__ import annotations
import json
import math
from typing import List

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  splitmethod : str,
                  k           : int,
                  m           : int,
                  root        : (NodeLeaf | NodeInternal | None) = None):
        self.k    = k
        self.m    = m
        self.splitmethod = splitmethod
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    
    def sort_split(self, data:List[Datum], split_coord:int):

        sorted_list = sorted(data, key = lambda d: d.coords[split_coord])
        
        midpoint = len(sorted_list) // 2
        midpoint_val = 0
        
        left_node = NodeLeaf(sorted_list[:midpoint])
        right_node = NodeLeaf(sorted_list[midpoint:])
        
        if len(sorted_list) % 2 == 1:
            midpoint_val = float(sorted_list[midpoint].coords[split_coord])
        else:
            midpoint_val = float((sorted_list[midpoint - 1].coords[split_coord] + sorted_list[midpoint].coords[split_coord]) / 2)
        
        node_internal = NodeInternal(split_coord, midpoint_val, left_node, right_node)

        return node_internal
    
    def overfull_spread(self, leaf:NodeLeaf):
        split_coord = -1
        max_split = -1
        
        if len(leaf.data) == 5:
            for i in range(self.k):
                min_num = leaf.data[0].coords[i]
                max_num = leaf.data[0].coords[i]
                for data in leaf.data:
                    if data.coords[i] < min_num:
                        min_num = data.coords[i]
                    elif data.coords[i] > max_num:
                        max_num = data.coords[i]
                
                split = max_num - min_num
                
                if split > max_split:
                    max_split = split
                    split_coord = i
        
        return self.sort_split(leaf.data, split_coord)
        
    def overfull_cycle(self, leaf:NodeLeaf, split_coord: int):
        
        return self.sort_split(leaf.data, split_coord)

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        
        if self.root == None:
            
            new_datum = Datum(point, code)
            
            add_node_leaf = [new_datum]
            
            self.root = NodeLeaf(add_node_leaf)
            
        else:
            
            prev = None
            curr = self.root
            
            go_left = None
            
            split_coord = 0
               
            while isinstance(curr, NodeInternal):
                
                prev = curr
                
                split_coord += 1
                
                if split_coord == self.k:
                    split_coord = 0
                
                if point[curr.splitindex] < curr.splitvalue:
                    go_left = True
                    curr = curr.leftchild
                else:
                    go_left = False
                    curr = curr.rightchild
            
            if isinstance(curr, NodeLeaf):
                
                new_datum = Datum(point, code)
                
                curr.data.append(new_datum)
                
                if len(curr.data) > self.m:
                    if self.splitmethod == "cycle":
                        curr = self.overfull_cycle(curr, split_coord)
                    else:
                        curr = self.overfull_spread(curr)
                        
                if prev:
                    if go_left:
                        prev.leftchild = curr
                    else:
                        prev.rightchild = curr
                else:
                    self.root = curr
            
            else:
                
                new_datum = Datum(point, code)
            
                add_node_leaf = [new_datum]
                
                if prev:
                    if go_left:
                        prev.leftchild = NodeLeaf(add_node_leaf)
                    else:
                        prev.rightchild = NodeLeaf(add_node_leaf)


    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        thisisaplaceholder = True

    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        leaveschecked = 0
        knnlist = []
        # The following return line can probably be left alone unless you make changes in variable names.
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]},indent=2))