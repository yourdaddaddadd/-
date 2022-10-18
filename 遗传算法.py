import numpy as np
import matplotlib.pyplot as plt
import random

ROAD_SIZE = 11
POP_SIZE = 50
JIAOCHA_RATE = 0.8
TUBIAN_RATE = 0.1
N_GENERATIONS = 40

def distance(x1, y1, x2, y2):
    dis = 0
    dis = np.sqrt(np.square(x1 - x2) + np.square(y1 - y2))
    return dis

def point(i):
    x = []
    y = []
    f = open("C:/Users/yangchen/Desktop/学习资料/人工智能/TSP/城市.txt", "r")
    content = f.readline()
    while content:
        a = content.split()
        x.append(int(float(a[1])))
        y.append(int(float(a[2])))
        content = f.readline()
    return x[i - 1], y[i - 1]


def select(road, fitness):
    sum = 0
    for i in range(len(fitness)):
        sum = sum + (fitness[i])
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=fitness/sum)
    return idx


def get_fitness(road):
    sum1 = []
    sum = 0
    for i in range(POP_SIZE):
        for j in range(len(road[i])):
            if j == len(road[i])-1:
                break
            x, y = point(road[i][j])
            x1, y1 = point(road[i][j + 1])
            sum = distance(x, y, x1, y1) + sum
        x0,y0=point(road[i][0])
        x2,y2=point(road[i][len(road[i])-1])
        sum = sum + distance(x0,y0,x2,y2)
        sum1.append(1/sum)
        sum = 0
    return sum1

def dis_sum(road):
    sum = 0
    for j in range(len(road)):
        if j == len(road)-1:
            break
        x, y = point(road[j])
        x1, y1 = point(road[j + 1])
        sum = distance(x, y, x1, y1) + sum
    x0,y0=point(road[0])
    x2,y2=point(road[len(road)-1])
    sum = sum + distance(x0,y0,x2,y2)
    return sum

def sampleplus(POP_SIZE, ROAD_SIZE):
    pop = []
    for i in range(POP_SIZE):
        road = random.sample(range(1, ROAD_SIZE + 1), ROAD_SIZE)
        pop.append(list(road))
    return pop


def jiaocha_and_tubian(road, JIAOCHA_RATE=0.8):
    new_pop = []
    for father in road:
        child1=father
        if np.random.rand() < JIAOCHA_RATE:
            mother = road[np.random.randint(POP_SIZE)]
            # 交叉位置
            jiaocha_point = np.random.randint(low=0, high=ROAD_SIZE)
            # 交叉
            child1 = father[0:jiaocha_point]
            child2 = mother[0:jiaocha_point]
            child1.extend(mother[jiaocha_point:ROAD_SIZE])
            child2.extend(father[jiaocha_point:ROAD_SIZE])
            # 修正子代,去除重复值
            index1 = []
            index2 = []
            for i in range(jiaocha_point,ROAD_SIZE):
                for j in range(jiaocha_point):
                    if child1[i] == child1[j]:  # 交叉点前面的交叉回来，从而不重复
                        index1.append(i)#
                    if child2[i] == child2[j]:
                        index2.append(j)
            num_index = len(index1)
            for i in range(num_index):
                child1[index1[i]], child2[index2[i]] = child2[index2[i]], child2[index1[i]]
        tubian(child1)
        new_pop.append(child1)
    return new_pop


def tubian(child, TUBIAN_RATE=0.5):
    child1=[]
    child1=child
    if np.random.rand() < TUBIAN_RATE:
        tubian_point1 = np.random.randint(0, ROAD_SIZE)
        tubian_point2 = np.random.randint(0, ROAD_SIZE)
        if tubian_point1 == tubian_point2:
            tubian_point2 = np.random.randint(0,ROAD_SIZE)
        x = child[tubian_point1]
        child[tubian_point1] = child[tubian_point2]
        child[tubian_point2] = x
    if dis_sum(child)>dis_sum(child1): #给突变一个限制，让突变往距离短的方向走
        tubian(child)
def print_draw(road):
    fitness = get_fitness(road)
    min_fitness = np.argmax(fitness)
    print("局部最短距离：", 1/fitness[min_fitness])
    print("局部最优的路径：", road[min_fitness])
    x=[]
    y=[]
    index=[]
    for i in road[min_fitness]:
        index.append(i)
        a,b = point(i)
        x.append(a)
        y.append(b)
    a1,b1=point(index[0])
    x.append(a1)
    y.append(b1)
    plt.plot(x, y,color='r')
    plt.scatter(x, y,color='b')
    plt.xlabel("x")
    plt.ylabel("y")
    for a, b in zip(x, y):  # 添加这个循坏显示坐标
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)
    plt.show()
    return road[min_fitness], 1/fitness[min_fitness]
if __name__ == "__main__":
    road = sampleplus(POP_SIZE, ROAD_SIZE)
    road1 = []
    roadlist = []
    fitlist = []
    for _ in range(N_GENERATIONS):
        road = jiaocha_and_tubian(road, JIAOCHA_RATE)
        fitness = get_fitness(road)
        idx = select(road, fitness)
        for i in range(len(idx)):
            road1.append(list(road[idx[i]]))
        road = road1
        road1 = []
        res1, res2 = print_draw(road)
        roadlist.append(list(res1))
        fitlist.append(res2)
    print('\n')
    print("所有局部最优路径：",roadlist)
    print('\n')
    print("所有局部最短距离：",fitlist)
    print('\n')
    min_fitness = np.argmin(fitlist)
    print("最优路径为：", roadlist[min_fitness])
    print("最短距离为：", fitlist[min_fitness])
    x=[]
    y=[]
    index=[]
    for i in roadlist[min_fitness]:
        index.append(i)
        a,b = point(i)
        x.append(a)
        y.append(b)
    a1,b1=point(index[0])
    x.append(a1)
    y.append(b1)
    plt.plot(x, y,color='r')
    plt.scatter(x, y,color='b')
    plt.xlabel("x")
    plt.ylabel("y")
    for a, b in zip(x, y):  # 添加这个循坏显示坐标
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=10)
    plt.show()