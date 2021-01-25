#导入模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import expon
import statsmodels.api as sm
import pylab
# filename='光明日报-stage3.json'
# filename='新华视点-stage3.json'
# filename='人民日报-stage1.json'
filename='stage2.json'
df1=pd.read_json(filename)
df2=pd.read_json('数据处理后：'+filename)


# filename2='stage4.json'
# df2=pd.read_json(filename2)


print(df2.shape)




# print('before')
# print(df1.shape)
# print('after')
# print(df2.shape)
# print('before 5')
# print(df1.head())
# print('after 5')
# print(df2.head())

# filename='光明日报-stage1.json'
# # (1184, 7)
# # Index(['微博地址:', '发布时间:', '微博标题:', '点赞数:', '评论数', '转发数', '评论'], dtype='object')
# df=pd.read_json(filename)
# print(df.shape)
# print(df.columns)

# filename='新华视点-stage1.json'
# (1601, 7)
# Index(['微博地址:', '发布时间:', '微博标题:', '点赞数:', '评论数', '转发数', '评论'], dtype='object')
# df=pd.read_json(filename)
# print(df.shape)
# print(df.columns)




# fre=pd.read_csv('frequency.csv')
# print(fre.shape)
# print(fre.index)
# # print(fre.columns)
#
# # print(fre['0.1'].sort_values())
# print(fre.sort_values(by='0.1'))


