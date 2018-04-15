class temp(object):
    def __init__(self, i):
        self.i = i

list1 = [temp(1), temp(1), temp(1)]
list2 =  list1.copy()

list2[0].i = 1337

list1[1] = None


#print(list1[0].i)
for i in range(0,3):
    if list1[i]:
        print(list1[i].i)

    print(list2[i].i)

print([x.i for x in list2[:3]])
print([x.i for (index,x) in enumerate(list2[:3])])
