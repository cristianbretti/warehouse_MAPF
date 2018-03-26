import numpy as np

# 0 - regular node
# 1 - obstacle node
# 2 - item pickup node
# 3 - drop off node

warehouse = np.array(
[
[0,0,0,0,0],
[3,0,1,2,1],
[0,0,1,1,1],
[0,0,1,2,1],
[0,0,0,0,0]
]
, dtype = np.int32)


straight_line = np.array(
[
[0,0,0,0,0,0,0,0,0]
]
, dtype = np.int32)
