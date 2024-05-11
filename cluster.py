from __future__ import annotations
import json
import math
from typing import List
import numpy as np

class Graph():
    def  __init__(self,
            nodecount : None):
        self.nodecount = nodecount
        # IMPORTANT!!!
        # Replace the next line so the Laplacian is a nodecount x nodecount array of zeros.
        # You will need to do this in order for the code to run!
        self.laplacian = np.zeros((nodecount, nodecount))

    # Add an edge to the Laplacian matrix.
    # An edge is a pair [x,y].
    def addedge(self,edge):
        first, second = edge

        self.laplacian[first][first] += 1
        self.laplacian[second][second] += 1
        self.laplacian[first][second] = -1
        self.laplacian[second][first] = -1

    # Don't change this - no need.
    def laplacianmatrix(self) -> np.array:
        return self.laplacian

    # Calculate the Fiedler vector and return it.
    # You can use the default one from np.linalg.eig
    # but make sure the first entry is positive.
    # If not, negate the whole thing.
    def fiedlervector(self) -> np.array:
        # Replace this next line with your code.
        e_vals, e_vecs = np.linalg.eig(self.laplacian)
        
        fied_eig = np.argsort(e_vals)[1]
        
        fvec = e_vecs[:, fied_eig]
        
        if fvec[0] < 0:
            fvec = -fvec
        # Return
        return fvec

    # Cluster the nodes.
    # You should return a list of two lists.
    # The first list contains all the indices with nonnegative (positive and 0) Fiedler vector entry.
    # The second list contains all the indices with negative Fiedler vector entry.

    def clustersign(self):
        # Replace the next two lines with your code.
        
        fvec = self.fvec()
        
        pind = []
        nind = []
        
        for i, val in enumerate(fvec):
            if val >= 0:
                pind.append(i)
            else:
                nind.append(i)
            
        # Return
        return([pind,nind])