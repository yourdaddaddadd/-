import random
import numpy as np
from math import e
from math import exp
import matplotlib.pyplot as plt
#10个城市的坐标
city_loc = [(12,89),(80,96),(22,87),(27,75),(100,83),
                 (44,25),(43,85),(81,61),(20,12),(79,83)]

T0 = 50000
T_end = 15
q = 0.98
L = 1000

#两个城市的距离
def dist(a, b):
    x1 = city_loc[a][0]
    x2 = city_loc[b][0]
    y1 = city_loc[a][1]
    y2 = city_loc[b][1]

    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return distance
#路程总长
def totaldistance(a):
    value = 0
    for j in range(10):
        if j == 9:
            break
        value += dist(a[j], a[j + 1])
    value += dist(a[9], a[0])
    return value

#初始化一个解 [0,1,2,3..30]
def init_ans():
    ans = []
    for i in range(10):
        ans.append(i)
    return ans
#产生新解
def creat_new(ans_before):
    ans_after = []
    for i in range(len(ans_before)):
        ans_after.append(ans_before[i])
    cuta = random.randint(0,9)
    cutb = random.randint(0,9)
    ans_after[cuta], ans_after[cutb] = ans_after[cutb], ans_after[cuta]#突变
    return ans_after

if __name__ == '__main__':
    ans0 =init_ans()
    T = T0
    cnt = 0
    trend = []
    while T > T_end:
        for i in range(L):
            newans = creat_new(ans0)#新解
            old_dist = totaldistance(ans0)#原本距离
            new_dist = totaldistance(newans)#新解距离
            df = new_dist - old_dist#计算差值
            if df >= 0:#说明新解更差
                rand = random.uniform(0,1)
                if rand < 1/(exp(df / T)):#？？
                    ans0 = newans
            else:
                ans0 = newans
        T = T * q
        cnt += 1
        now_dist = totaldistance(ans0)
        trend.append(now_dist)
        #print(cnt,"次降温，温度为：",T," 路程长度为：", now_dist)
    distance = totaldistance(ans0)
    print(distance, ans0)
    plt.plot(trend)
    plt.show()
