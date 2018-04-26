from WHCA import *
from DecisionTree import *

file_name1 = "all_first.txt"
file_name2 = "all_coordinates.txt"
file_name3 = "all_coordinates_small.txt"
file_name4 = "all_area.txt"

print("     " + file_name1 + ":")
for i in range(1, 7):
    DecisionTree(file_name1, i)


print("     " + file_name2 + ":")
for i in range(1, 7):
    DecisionTree(file_name2, i)


print("     " + file_name3 + ":")
for i in range(1, 7):
    DecisionTree(file_name3, i)


print("     " + file_name4 + ":")
for i in range(1, 7):
    DecisionTree(file_name4, i)
