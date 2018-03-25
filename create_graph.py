import numpy as np
from small_warehouse import warehouse as wh
from BasicNode import *

graph = np.ndarray((wh.shape), dtype=BasicNode)

index = 0
for (i,j), value in np.ndenumerate(wh):
        graph[i][j] = BasicNode(index, value)
        index += 1

print(graph)
