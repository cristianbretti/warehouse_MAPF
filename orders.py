import random
from functions import *
from warehouse import warehouse
random.seed(9501020078)

#small_order_list = [[104,104],[166,266,625],[920,1182,999],[1182,1319]]
small_order_list = [[104,1182,357,206,453,1123]]
#small_order_list = [[104],[104]]

#small_order_list = [[104],[106],[108],[110],[112],[210],[110,110,110,110],[112,110,110,110],[210,692,694,939],[1190,1344]]

#big_order_list = [[[104,1182,357,206,453,1123]]]
#big_temp = [[[206,357]]] # works in under 1 sec
big_temp = [[[357],[206],[839],[104]]]
#big_temp = [[[839]]]


left_pickups = [104,106,108,110,112,
            202,204,206,208,210,
            349,351,353,355,357,
            447,449,451,453,455,
            594,596,598,600,602,
            692,694,696,698,700,
            839,841,843,845,847,
            937,939,941,943,945,
            1084,1086,1088,1090,1092,
            1182,1184,1186,1188,1190]

_, temp, _ = create_Astar_graph(warehouse)
right_pickups = [x.id for x in temp if x.id not in left_pickups]

all_pickups = left_pickups + right_pickups


def simulate_8020_orders(num_orders, average_item_per_order):
    orders = []
    for i in range(0, num_orders):
        current_order = []
        while True:
            if random.random() > 0.2:
                current_order.append(left_pickups[random.randint(0, len(left_pickups)-1)])
            else:
                current_order.append(right_pickups[random.randint(0, len(right_pickups)-1)])

            if random.randint(1, average_item_per_order) == average_item_per_order:
                orders.append(current_order)
                break
    return orders

def simulate_uniform_orders(num_orders, average_item_per_order):
    orders = []
    for i in range(0, num_orders):
        current_order = []
        while True:
            current_order.append(all_pickups[random.randint(0, len(all_pickups)-1)])

            if random.randint(1, average_item_per_order) == average_item_per_order:
                orders.append(current_order)
                break
    return orders

def simulate_big_order_list(uniform, num_simulations, num_orders, average_item_per_order):
    big_order_list = []
    for i in range(0, num_simulations):
        if uniform:
            big_order_list.append(simulate_uniform_orders(num_orders, average_item_per_order))
        else:
            big_order_list.append(simulate_8020_orders(num_orders, average_item_per_order))
    return big_order_list


def control_check_order_sim():
    test = simulate_uniform_orders(20, 3)
    print(test)
    avg_size = 0
    for i in range(0, len(test)):
        avg_size += len(test[i])
    print("average order size is: %.2f" % (avg_size/len(test)))

    pop_item = 0
    total_items = 0
    for i in range(0, len(test)):
        for j in range(0, len(test[i])):
            total_items += 1
            if test[i][j] in left_pickups:
                pop_item += 1

    print("%d %% of the items belong to popular ones" % ((pop_item/total_items)*100))
