#导入模块
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import expon
import statsmodels.api as sm
import pylab
import xlrd

# df = pd.read_json('人民日报.json')
df = pd.read_excel("stage4-检验.xlsx", sheet_name='JSON',usecols=[0,1, 2, 3, 4])
# (5401, 5)
context=2
rel=4
sta=100
end=sta+100


# s1 = pd.Series([1,'a',5.2,7])
# print(s1[3])

# print(df.columns)#Index(['微博地址:', '发布时间:', '微博标题:', '转发数', '疫情相关 1 相关  0 无关'], dtype='object')
# print(df)
# print(df.shape)
# print(df.columns)#Index(['微博地址:', '微博内容:', '点赞数:', '评论数', '转发数', '评论'], dtype='object')
# print(df.loc[1])#字典输出

# '病','医'
# 出院？ 检验？医疗机构？ 医院？采集？ 采样？ 患者 医生？ 医护人员？
rela=['病例','医学观察 ','病毒','流行病','疫','确诊','新增','无症状','检测','感染','核酸','隔离','阳性','阴性'
    ,'密切接触', '新冠','肺炎','重症','轻症''新型','高风险','卫健','消毒','冠状','检测','抗体','口罩','防护',
      '双检','血清','防护服','中风险','公共卫生','复课','停课','居家','疾控','恢复开放','恢复通车','传染病',
      '复工','复产','康复患者','康复']
# for i in range(0,len(df)):
#     s = df.loc[i]
#     st =s[context]
#     # print(st)
#     flag = False#不是疫情相关
#     for re in rela:
#         # print(st.find(re))
#         if(st.find(re)!=-1):
#             flag=True
#             # print('?')
#             break
#     if(flag==False):
#         df = df.drop([i])
#         # print(df)
#

relate=0
for i in range(sta,end):
    s = df.loc[i]
    st =s[context]
    # print(st)
    flag = 0#不是疫情相关
    for re in rela:
        # print(st.find(re))
        if(st.find(re)!=-1):
            flag=1
            # print('?')
            break
    if(flag==s[rel]):
        relate+=1
        # print(df)
    else:
        print(i)

pre = "%.2f%%" % relate

print(pre)

for re in rela:
    st=df.loc[112][context]
    if (st.find(re)!= -1):
        print(st[st.find(re)])


# print(df.shape)
# df=df.drop([0])
# df=df.drop([500])
# df=df.drop([1000])

# df.index = range(len(df))#index重新排序
# # df=df.reset_index(drop=True, inplace=True)
# df.to_json(orient='index')
# df.to_json('检验后.json')
#

# df.to_json('2.json')
