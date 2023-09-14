# This is a sample Python script.
from datetime import datetime
from itertools import combinations

import pymysql


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#计算时间差值
def timesubw(a, b):
    datetime1 = datetime.strptime(a, "%Y/%m/%d %H:%M:%S")
    datetime2 = datetime.strptime(b, "%Y/%m/%d %H:%M:%S")
    if(datetime1 >= datetime2):
        delta = datetime1 - datetime2
        return (delta.seconds)
    else:
        delta = datetime2 - datetime1
        return (-delta.seconds)

#读取数据库数据
conn = pymysql.connect(host = 'localhost', user = 'root', password = '517447', db = 'time2', port = 3306, charset ='utf8')
cur = conn.cursor()
cur.execute('SELECT * FROM timelist')
result = cur.fetchall()
#将检测到数据的车牌号放入一个集合
car_set = set()
for i in result:
    if i[1] != '车牌':
        car_set.add(i[1])
car_list = list(car_set)
#for i in range(1, 101):
print(len(car_list))
conn.close()  # 使用完后记得关掉

#用两个字典分别存储两天的车牌号与其对应的数据
cardic1 = dict() #定义一个字典存放不同车的信息
cardic2 = dict()
for i in car_list:
    cartro1 = list()
    cartro2 = list()
    for u in result:
        if (u[1] == i) and (u[3][7]=='1'):
            cartro1.append(u)
        elif(u[1] == i) and (u[3][7]=='2'):
            cartro2.append(u)

    if(len(cartro1) >1):
       cardic1[i] = cartro1
    if(len(cartro2) >1):
       cardic2[i] = cartro2

#计算所需车牌号的时间差值
for carname in cardic2.keys():
    subdict=dict()
    for i in range(0, len(cardic2[carname])-1):

        for u in range(1,  len(cardic2[carname])-i):
            time = timesubw(cardic2[carname][i][3], cardic2[carname][i+u][3])
            if abs(time) < 500:
                if time >= 0:
                    key = cardic2[carname][i][0] + '--' + cardic2[carname][i + u][0]
                    if key in subdict:
                        subdict[key].append(time)
                    else:
                        subdict[key]=[time]
                else:
                    key = cardic2[carname][i+u][0] + '--' + cardic2[carname][i][0]
                    if key in subdict:
                        subdict[key].append(-time)
                    else:
                        subdict[key] = [-time]
    print("%s :"% carname)
    print(subdict)
    #print("\n")
    #测试上传github

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
