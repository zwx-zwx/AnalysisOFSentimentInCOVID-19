import pandas as pd
import jieba
import os
from cntopic import Topic
import csv

filename ='stage3.csv'
with open('每条'+filename, 'w', newline='') as wr:
    writer = csv.writer(wr)
    with open(filename, 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            # 行号从1开始
            dic=reader.line_num, row[7]
            # print(dic+"1")
            # print(dic[1])
            str = dic[1]
            list = str.split("'")
            # print(list)
            for str in list:
                if ((len(str) > 1)&(str!=', ')):
                    try:
                    # for row in list:
                        writer.writerow([str])
                    except UnicodeEncodeError:
                        pass

                # else:
                #     list.remove(str)
            # print(str)
            # print(list)




        # for key in dic[1]:
        #     # for str in key:
        #     #     print(str)
        #     print(key)
# str=又暴跌，对中国发展是个千载难逢的良机。']"
# list = str.split("'")
# print(list)
# for str in list:
#     if(len(str)>1):
