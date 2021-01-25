#导入模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import expon
import statsmodels.api as sm
import pylab
# %matplotlib inline

# df = pd.read_json('人民日报.json')
# # print(df.shape)
# # print()
# # print(df.columns)
# # print()
# # print(df.index)
# # print()
# # print(df.dtypes)
# comment=df['评论数']
# # likes =df['点赞数:']
# # c_l = df[['评论数','点赞数:']]
# # print(c_l.cov())
# # print(c_l.corr())

df = pd.read_json('人民日报-stage4.json')
comment=df['评论数']
# print(df.columns)#Index(['微博地址:', '发布时间:', '微博标题:', '点赞数:', '评论数', '转发数', '评论'], dtype='object')
# 2440.518237363451
# 6358.825406071377


# # print(comment)
# comment.plot()
# # comment.hist()
# plt.show()

fig = plt.figure(figsize = (10,6))
ax1 = fig.add_subplot(2,1,1)  # 创建子图1
ax1.scatter(comment.index, comment.values)
# ax1.plot(comment)
# comment.plot(ax1)
plt.grid()#网格而已


# print(df.shape)
all=df.shape[0]
print(all)
context='评论数'
for i in range(0,len(df)):
    s = df.loc[i]
    st =s[context]
    # print(st)
    if(st<400):
        df = df.drop([i])
    # flag = False#不是疫情相关
    # for re in rela:
    #     # print(st.find(re))
    #     if(st.find(re)!=-1):
    #         flag=True
    #         # print('?')
    #         break
    # if(flag==False):
    #     df = df.drop([i])
    #     # print(df)

last=df.shape[0]
pre = "%.2f%%" % (last/all*100)
print(pre)

comment=df['评论数']
ax2 = fig.add_subplot(2,1,2)  # 创建子图1
# ax1.plot(comment,color='red')
ax1.scatter(comment.index, comment.values,color='red')

# comment.plot(ax1)
plt.grid()#网格而已
plt.show()



# df.index = range(len(df))#index重新排序
# df.to_json(orient='index')
# df.to_json('main.json')


# fig = plt.figure(figsize = (10,6))
# ax1 = fig.add_subplot(2,1,1)  # 创建子图1
# ax1.scatter(comment.index, comment.values)
# plt.grid()#网格而已
# ax2 = fig.add_subplot(2,1,2)  # 创建子图2
# comment.hist(bins=30,alpha = 0.5,ax = ax2)
# comment.plot(kind = 'kde', secondary_y=True,ax = ax2)
# plt.grid()
# plt.show()


# qq
# sm.qqplot(comment, line='s')
# pylab.show()


# kstest方法：KS检验，参数分别是：待检验的数据，检验方法（这里设置成norm正态分布），均值与标准差
# 结果返回两个值：statistic → D值，pvalue → P值
# p值大于0.05，为正态分布
# H0:样本符合
# H1:样本不符合
# 如何p>0.05接受H0 ,反之
# """# """结果是KstestResult(statistic=0.01441344628501079, pvalue=0.9855029319675546)，p值大于0.05为正太分布
# u = comment.mean()  # 计算均值
# std = comment.std()  # 计算标准差
# print(u)
# print(std)
# print(stats.kstest(comment, 'norm', (u, std)))

# plt.hist(comment,100,normed=True,facecolor='g',alpha=0.9)
# plt.show()
# print(comment.skew())#%偏度计算
# print(comment.kurt())#%峰度计算
# 正态性检验要求严格通常无法满足，如果峰度绝对值小于10并且偏度绝对值小于3，则说明数据虽然不是绝对正态，但基本可接受为正态分布。
# 12.635873984853069
# 218.27319294066083

# frame = pd.DataFrame(np.arange(16).reshape(4, 4),
#                      index=['white', 'black', 'red', 'blue'],
#                      columns=['up', 'down', 'right', 'left'])
# print(frame)
# df.to_json('frame.json')





