from WHCA import *
from DecisionTree import *
from functions import *

file_name1 = "all_first.txt"
file_name2 = "all_coordinates.txt"
file_name3 = "all_coordinates_small.txt"
file_name4 = "all_area.txt"

f = open("all_first.txt", 'r')

x = read_lines_from_file(f)

for i in range(0, len(x)):
    for j in range(i+1, len(x)):
        if x[i][:-1] == x[j][:-1]:
            print("line %d and %d eq" % (i, j))


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
