//出租车司机决策的Python实现//
#输入参数
import numpy as np
w = np.array([0.085834,0.49778,0.13915,0.22416,0.053081]) #输入各因素权重向量
lamda = np.array([[0.9,1.1],[0.85,1.16],[0.92,1.1],[0.9,1.12],[1,1.1]]) #输入各因素下不同情况的校正系数
season = 0 #0为淡季，1为旺季
rush_hour = 0 #0为低峰时段，1为高峰时段
weekend = 0 #0为工作日，1为周末
climate = 0 #0为适宜天气，1为恶劣天气
event = 0 #0为无重大活动，1为有重大活动
ncar = 50  #司机观测到的蓄车池内车辆数
nflight = 20  #司机观测到未来1小时内降落航班数
np = 120 #平均一架航班的旅客数目
t0 = 0.01  #乘客平均上车时间
S0 = 40 #机场出发旅客平均乘车里程（KM）
T = 0.8 #机场出发旅客平均乘车时长
b = 1  #市区拥堵系数
t1 = 0.5 #从机场返回市区平均用时
t2 = 0.2 #市区内司机接客等待平均用时
v_city = 30 #市区内道路平均时速（KM/小时）

#计算各项权重系数
factor = [season,rush_hour,weekend,climate,event]
l_factor = []
for i in range(0,5):
    l_factor.append(lamda[i][factor[i]]) #得到对应情况下的校正系数
a_mean = 0.483 #根据历史数据得到的均值
l_factor_1 = np.array([l_factor]).T
a = np.dot(w,l_factor_1)
a = float(a)*a_mean#得到该情况下a的值
#进行决策
if S0/T <= v_city:
    print("警告：不满足模型假设（机场行程平均时速大于市区行程平均时速）") #检验输入参数是否合理

if rush_hour == 1:
   wait_airport_time = ncar*t0
else:
   wait_airport_time = ncar*t0 + 2*ncar/(np*nflight*a)    
print("机场等待时间为：",wait_airport_time,"小时" )
    
wait_city_time = t1*b+t2   
print("市区空载时间为：",wait_city_time,"小时" )
if  wait_airport_time <=  wait_city_time:
    print("机场等待时间小于市区空载时间，最优决策为留在机场")
else:
    S_city = (wait_airport_time+T-wait_city_time)*b*v_city
    print("机场载客期望里程为：",S0,'\n',"市区载客期望里程为：",S_city)
    if S0 >= S_city:
        print("最优决策为留在机场")
    else:
        print("最优决策为返回市区")
