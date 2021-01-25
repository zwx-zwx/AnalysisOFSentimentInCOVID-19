import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import expon
import statsmodels.api as sm
import pylab
import xlrd
import json

#可变项
# filename='新华视点-stage3.json'
name='stage3'
filename=name+'.json'
# filename="人民日报.json"
col_comment='评论数'
col_main_context='微博标题:'
# col_main_context="微博内容:"

threshold=400
rela=['病例','医学观察 ','病毒','流行病','疫','确诊','新增','无症状','检测','感染','核酸','隔离','阳性','阴性'
    ,'密切接触', '新冠','肺炎','重症','轻症''新型','高风险','卫健','消毒','冠状','检测','抗体','口罩','防护',
      '双检','血清','防护服','中风险','公共卫生','复课','停课','居家','疾控','恢复开放','恢复通车','传染病',
      '复工','复产','康复患者','康复','返工']




#读入
# df = pd.read_json('人民日报.json')
# df = pd.read_excel("stage4-检验.xlsx", sheet_name='JSON',usecols=[0,1, 2, 3, 4])
df = pd.read_json(filename,encoding='utf-8')


#筛选出重点新闻，阈值400
all=df.shape[0]
# print(all)
for i in range(0,len(df)):
    s = df.loc[i]
    st =s[col_comment]
    if(st<threshold):
        df = df.drop([i])


df.index = range(len(df))#index重新排序
#筛选出疫情相关
for i in range(0,len(df)):
    s = df.loc[i]
    st =s[col_main_context]
    flag = False#不是疫情相关
    for re in rela:
        if(st.find(re)!=-1):
            flag=True
            break
    if(flag==False):
        df = df.drop([i])


#导出

df.index = range(len(df))#index重新排序
# df.to_json(orient='index')
# df.to_json('数据处理后：'+filename,encoding="utf8")
# # df.to_json("test.txt")
# df.to_csv(name+".csv", encoding="utf_8_sig")

# df.to_json('数据处理后：'+filename,orient='index', force_ascii=True)
# df_json = df.to_json(orient='index', force_ascii=False)
# json.loads(df_json)

# json_dict = df.to_dict(orient = "dict")  # 返回结果： {'col 1': {'row 1': 'a', 'row 2': 'c'}, 'col 2': {'row 1': 'b', 'row 2': 'd'}}
# json.dumps(json_dict)
# json.load('数据处理后：'+filename)


