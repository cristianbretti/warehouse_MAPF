import matplotlib.pyplot as plt
from functions import *
import numpy as np
import matplotlib as mpl
mpl.style.use('seaborn-poster')

def plot_data(results_x, prev_x=1, name=None):
    x = [i for i in range(prev_x, len(results_x[0])+prev_x)]
    DKBR_line, = plt.plot(x, [p for p in results_x[1]], 'C1', lw=0.8, label="DKBR")
    Random_line, = plt.plot(x, [p for p in results_x[2]], 'C2', lw=0.8, label="Random")
    WHCA_line, = plt.plot(x, [p for p in results_x[0]],'C3', lw=0.8, label="WHCA*")
    plt.legend(handles=[WHCA_line, DKBR_line, Random_line])
    plt.ylabel("Cost")
    plt.xlabel("Trial number")
    plt.title('Cost for each algorithm')
    if name:
        plt.savefig(name)
    plt.show()

def plot_markers(results_x):
    x = [i for i in range(1, len(results_x[0])+1)]
    DKBR_line, = plt.plot(x, [p for p in results_x[1]], 'C1.', lw=0.8, label="DKBR")
    Random_line, = plt.plot(x, [p for p in results_x[2]], 'C2-', lw=0.8, label="Random")
    WHCA_line, = plt.plot(x, [p for p in results_x[0]],'C3', lw=0.6, label="WHCA*")
    plt.legend(handles=[WHCA_line, DKBR_line, Random_line])
    plt.ylabel("Difference to WHCA*")
    plt.xlabel("Trial number")
    plt.show()


result_file = open("results.txt", 'r')
tree_fail_file = open("tree_fail_file.txt", 'r')

results_x = read_lines_from_file(result_file)
tree_fail_x = read_lines_from_file(tree_fail_file)


major = sorted(zip(results_x[0],results_x[1],results_x[2], tree_fail_x[0], tree_fail_x[1],tree_fail_x[2]), key=lambda pair: pair[0])

data_first = []
data_first.append([x for x, _, _, _, _, _ in major])
data_first.append([x for _, x, _, _, _, _  in major])
data_first.append([x for _, _, x, _, _, _  in major])

tree_fail_data = []
tree_fail_data.append([x for _, _, _, x, _, _ in major])
tree_fail_data.append([x for _, _, _, _, x, _  in major])
tree_fail_data.append([x for _, _, _, _, _, x  in major])

max_count = 1
data = [[],[],[]]
count = 0
accum1 = 0
accum2 = 0
accum3 = 0
for i in range(0, len(data_first[0])):
    accum1 += data_first[0][i]
    accum2 += data_first[1][i]
    accum3 += data_first[2][i]
    count += 1
    if count == max_count:
        data[0].append(accum1/count)
        data[1].append(accum2/count)
        data[2].append(accum3/count)
        accum1 = 0
        accum2 = 0
        accum3 = 0
        count = 0

if count != 0:
    data[0].append(accum1/count)
    data[1].append(accum2/count)
    data[2].append(accum3/count)


data1 = [[],[],[]]
data2 = [[],[],[]]
data3 = [[],[],[]]
data4 = [[],[],[]]
data5 = [[],[],[]]

increment = int(len(data[0])/5)

data1[0] = data[0][:increment]
data2[0] = data[0][increment:2*increment]
data3[0] = data[0][2*increment:3*increment]
data4[0] = data[0][3*increment:4*increment]
data5[0] = data[0][4*increment:len(data[0])]
data1[1] = data[1][:increment]
data2[1] = data[1][increment:2*increment]
data3[1] = data[1][2*increment:3*increment]
data4[1] = data[1][3*increment:4*increment]
data5[1] = data[1][4*increment:len(data[1])]
data1[2] = data[2][:increment]
data2[2] = data[2][increment:2*increment]
data3[2] = data[2][2*increment:3*increment]
data4[2] = data[2][3*increment:4*increment]
data5[2] = data[2][4*increment:len(data[2])]

plot_data(data, name='all_tests.jpg') # THIS NOE
#plot_data(data1)
#plot_data(data2, increment)
plot_data(data3, 2*increment, name='zoomed.jpg') # THIS ONE
#plot_data(data4, 3*increment)
#plot_data(data5, 4*increment)

difference_data = [[],[],[]]
difference_data[0] = np.subtract(data[0], data[0])
difference_data[1] = np.subtract(data[0], data[1])
difference_data[2] = np.subtract(data[0], data[2])

#plot_markers(difference_data) # ONE OF THESE

x = [1]
f, (ax, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[4, 1]})

y_DKBR = sum(tree_fail_data[1])-sum(tree_fail_data[0])
y_misses = sum(tree_fail_data[0])
ax.bar([0.8], [y_DKBR], width=0.3,color='C1',align='center')
ax.bar([0.8], [y_misses], bottom=y_DKBR, width=0.3,color='C4',align='center')
ax.bar([1.2], [sum(tree_fail_data[2])],width=0.3,color='C2',align='center')

ax2.bar([0.8], [y_DKBR], width=0.3,color='C1',align='center')
ax2.bar([0.8], [y_misses], bottom=y_DKBR, width=0.3,color='C4',align='center')
ax2.bar([1.2], [sum(tree_fail_data[2])],width=0.3,color='C2',align='center')

ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + 7.5*d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + 7.5*d), **kwargs)  # bottom-right diagonal

ax.set_ylim(10000, 12000)  # outliers only
ax2.set_ylim(0, 100)

ax.text(0.783, sum(tree_fail_data[1]) + 10, str(sum(tree_fail_data[1])), color='black', fontweight='bold')
ax.text(0.783, y_DKBR + 10, str(y_DKBR), color='black', fontweight='bold')
ax.text(0.72, y_DKBR + 900, "Non-applicable rule picked", color='black', fontweight='bold')
ax.text(1.183, sum(tree_fail_data[2]) + 10, str(sum(tree_fail_data[2])), color='black', fontweight='bold')

ax.set_ylabel("Collisions")
ax2.set_ylabel("Collisions")
ax.set_title("Number of collisions")
plt.xticks([0.8, 1.2], ['DKBR', 'Random'])

plt.savefig('number_of_collisions.jpg')
plt.show()

WHCA_avg = 896.698
DKBR_avg = 901.076
RND_avg = 900.523

x = [1]
ax = plt.subplot(111)
ax.bar([0.8], [WHCA_avg],width=0.2,color='C3',align='center')
ax.bar([1], [DKBR_avg],width=0.2,color='C1',align='center')
ax.bar([1.2], [RND_avg],width=0.2,color='C2',align='center')
ax.set_ylim(890, 902)  # outliers only

ax.text(0.77, WHCA_avg + .25, str(WHCA_avg), color='C3', fontweight='bold')
ax.text(0.97, DKBR_avg + .25, str(DKBR_avg), color='C1', fontweight='bold')
ax.text(1.17, RND_avg + .25, str(RND_avg), color='C2', fontweight='bold')

plt.ylabel("Cost")
plt.xticks([0.8, 1, 1.2], ['WHCA*', 'DKBR', 'Random'])
plt.title('Average cost')

plt.savefig('average_cost.jpg')
plt.show()
