#导入模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# %matplotlib inline

# df = pd.read_json('purchases.json')

# if __name__=="__main__":
#构造一组随机数据
s = pd.DataFrame(np.random.randn(1000)+10,columns = ['value'])
# s[ 'value' ].plot()
# s['value' ].hist()
# print(s['value' ].value_counts())

# kstest方法：KS检验，参数分别是：待检验的数据，检验方法（这里设置成norm正态分布），均值与标准差
# 结果返回两个值：statistic → D值，pvalue → P值
# p值大于0.05，为正态分布
# H0:样本符合
# H1:样本不符合
# 如何p>0.05接受H0 ,反之
# """
u = s['value'].mean()  # 计算均值
std = s['value'].std()  # 计算标准差
print(stats.kstest(s['value'], 'norm', (u, std))
)

#
# #画散点图和直方图
# fig = plt.figure(figsize = (10,6))
#
# ax1 = fig.add_subplot(2,1,1)  # 创建子图1
# ax1.scatter(s.index, s.values)
# plt.grid()#网格而已
#
#
# ax2 = fig.add_subplot(2,1,2)  # 创建子图2
# s.hist(bins=30,alpha = 0.5,ax = ax2)
# s.plot(kind = 'kde', secondary_y=True,ax = ax2)
# plt.grid()
#
# plt.show()





# import matplotlib as mpl
# import matplotlib.pyplot as plt
# x = [1,3,5,7]
# y = [4,9,6,8]
# plt.plot(x,y)
# plt.show()