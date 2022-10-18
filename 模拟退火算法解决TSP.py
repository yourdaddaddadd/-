import numpy as np
import matplotlib.pyplot as plt
import random
import math
T = 2000
dt=0.99
eps = 1e-14
dx=0
process=[]
city_loc = [(12,89),(80,96),(22,87),(27,75),(100,83),
                 (44,25),(43,85),(81,61),(20,12),(79,83)]
road = random.sample(range(0, 10), 10)
print(road)
def tubian(road):
    point1=np.random.randint(0,9)
    point2=np.random.randint(0,9)
    if point1==point2:
        point2=np.random.randint(0,9)
    a = road[point1]
    road[point1]=road[point2]
    road[point2]=a
    return road
def dis(x1, y1, x2, y2):
    dis = 0
    dis = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))
    return dis
def distance(road):
    sum=0
    for i in range(len(road)):
        if i == len(road)-1:
            break
        sum = sum + dis(city_loc[road[i]][0],city_loc[road[i]][1],city_loc[road[i+1]][0],city_loc[road[i+1]][1])
    sum = sum + dis(city_loc[road[0]][0],city_loc[road[0]][1],city_loc[road[9]][0],city_loc[road[9]][1])
    return sum
while T>eps:
    now_road=road.copy()
    old_road=road.copy()
    tubian(now_road)
    df=distance(now_road)
    f=distance(old_road)
    if f>df:
        road=now_road
        process.append(df)
    else:
        if math.exp((f-df)/T)>np.random.rand():
            road=now_road
            process.append(df)
        else:
            process.append(f)
    T=T*dt
print(road)
print(distance(road))
x=[]
y=[]
index=[]
for i in road:
    index.append(i)
    a = city_loc[road[i]][0]
    b = city_loc[road[i]][1]
    x.append(a)
    y.append(b)
a1=city_loc[road[index[0]]][0]
b1=city_loc[road[index[0]]][1]
x.append(a1)
y.append(b1)
plt.figure()
plt.plot(x, y,color='r')
plt.scatter(x, y,color='b')
plt.xlabel("x")
plt.ylabel("y")
for a, b in zip(x, y):  # 添加这个循坏显示坐标
    plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)
plt.show()

plt.figure()
plt.plot(process)
plt.show()