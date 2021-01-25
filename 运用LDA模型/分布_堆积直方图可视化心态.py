import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False


colors = ["#006D2C", "#31A354","#74C476","#66c2a5","#8da0cb"]
colors=['olive','purple','cyan','red','blue', 'gray','pink','brown','orange','green']


df = pd.read_excel('堆积直方图可视化心态.xlsx')
print(df.index)
# print(df.shape)
# print(df.columns)
# RangeIndex(start=0, stop=4, step=1)
# (4, 6)
# Index(['Unnamed: 0', '心态a', '心态b', '心态c', '心态d', '心态e'], dtype='object')
# pdf =df.pivot(index='时间', columns='心态', values='Value')#$函数接受索引的参数（x轴和Y轴）
# df.loc[:,['Attitude_a', 'Attitude_b', 'Attitude_c', 'Attitude_d', 'Attitude_e']].plot.bar(stacked=True, color=colors, figsize=(12,7))
# ['stage1','stage2','stage3','stage4']
df.loc[:,['事不关己','困惑质疑','痛苦悲伤'	,'愤愤不平','焦虑恐慌','担忧关切','美好期盼','感动赞美','轻松愉悦','坚定信任']].plot.bar(stacked=True, color=colors, figsize=(12,7))

plt.show()