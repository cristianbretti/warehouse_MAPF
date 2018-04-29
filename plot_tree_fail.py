import matplotlib.pyplot as plt
from functions import *
import numpy as np

tree_fail_file = open("tree_fail_file.txt", 'r')

tree_fail_x = read_lines_from_file(tree_fail_file)

# plt.plot([i for i in range(1, len(results_x[0])+1)], [p for p in results_x[0]], 'b.')
# plt.plot([i for i in range(1, len(results_x[1])+1)], [p for p in results_x[1]], 'r.')
# plt.plot([i for i in range(1, len(results_x[2])+1)], [p for p in results_x[2]], 'g.')
# plt.show()

data = []
data.append([x for x, _, _ in sorted(zip(results_x[0],results_x[1], results_x[2]), key=lambda pair: pair[0])])
data.append([x for _, x, _ in sorted(zip(results_x[0],results_x[1], results_x[2]), key=lambda pair: pair[0])])
data.append([x for _, _, x in sorted(zip(results_x[0],results_x[1], results_x[2]), key=lambda pair: pair[0])])

#print(data)




#data = results_x

rows = ['WHCA', 'DKBR', 'Random']
columns = ['Trial %d' % x for x in range(1, len(results_x[0]) + 1)]

#values = np.arange(0, 6000, 1000)
#print(values)
#value_increment = 2000

# Get some pastel shades for the colors
colors = plt.cm.tab20c(np.linspace(0.2, 0.5, len(rows) + 0.2))
n_rows = len(data)

index = np.arange(len(columns)) + 1.0
index_offset = [-0.2,0,0.2]
bar_width = 0.2

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):

    x_val = [x+index_offset[row] for x in index]
    plt.bar(x_val, data[row], width=bar_width, bottom=None, color=colors[row], align='center')
    y_offset = y_offset + data[row]
    #cell_text.append(['%d' % (x) for x in y_offset])
    cell_text.append(data[row])
# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
#cell_text.reverse()

table_colors = []
table_colors.append(colors[2])
table_colors.append(colors[1])
table_colors.append(colors[0])
# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=table_colors,
                      colLabels=columns,
                      loc='bottom')

# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)

plt.ylabel("Cost")
#plt.yticks(values * value_increment, ['%d' % val for val in values])
plt.xticks([])
plt.title('Cost for each Trial ')

plt.show()
