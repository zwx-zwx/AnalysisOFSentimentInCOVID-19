import pandas as pd
import jieba
import os
from cntopic import Topic
import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import jieba.posseg as psg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
if __name__ == '__main__':
    ntop=8
    filenmae='每条stage4.csv'
    filenmae2=str(ntop)+'_topics '+filenmae

    df = pd.read_csv(filenmae,encoding='utf-8')
    # print(df.head())
    # print(df['label'].value_counts())
    # print(df.columns)
    # 2. 准备数据

    def split(parameter):
        stopword = []
        with open('stoplist.txt', 'r', encoding='utf-8') as s:
            for line in s.readlines():
                l = line.strip()
                if l == '\\n':  # 换行符
                    l = '\n'
                if l == '\\u3000':  # 制表符
                    l = '\u3000'
                stopword.append(l)
        n = [x.word for x in psg.cut(parameter) if not x.flag.startswith('n')]  # 去名词
        x = np.array(n)
        y = np.array(stopword)
        z = x[~np.in1d(x, y)]  # 去停用词
        k = [i for i in z if not i.isnumeric()]  # 去数字
        m = [i for i in k if len(i) > 1 or i == '']  # 去长度为1的词
        return np.array(m).tolist()


    def text2tokens(raw_text):
        #将文本raw_text分词后得到词语列表
        # tokens = jieba.lcut(raw_text)
        tokens = split(raw_text)
        return tokens

    # #对content列中所有的文本依次进行分词
    documents = [text2tokens(txt)
                 for txt in df['评论']]
    # 显示前5个document
    # # print(documents[:5])

    # # 3. 训练lda模型
    topic = Topic(cwd=os.getcwd()) #构建词典dictionary
    topic.create_dictionary(documents=documents) #根据documents数据，构建词典空间
    topic.create_corpus(documents=documents) #构建语料(将文本转为文档-词频矩阵)
    # topic.create_corpus(documents=tf) #构建语料(将文本转为文档-词频矩阵)
    topic.train_lda_model(n_topics=ntop) #指定n_topics，构建LDA话题模型

    # 4. 使用LDA模型
    document = jieba.lcut('北京的朋友还是要加强防范，不能掉以轻心，在公共场合戴好口罩我在南京默默支持你们，陪你们共渡难关，等疫情结束欢迎来南京做客')

    # 4.2 预测document对应的话题

    # print(topic.get_document_topics(document))

    # 4.3 显示每种话题与对应的特征词之间关系¶
    with open(filenmae2, 'w', newline='',encoding='utf8') as wr:
        writer = csv.writer(wr)
        # try:
        for r in topic.model.show_topics():
            writer.writerow(r)
        # except UnicodeEncodeError:
        #     pass

    # 4.4 话题分布情况
    # print(topic.topic_distribution(raw_documents=df['评论']))#<class 'pandas.core.series.Series'>

    s = topic.topic_distribution(raw_documents=df['评论'])
    #画散点图和直方图
    # fig = plt.figure(figsize = (10,6))
    #
    # ax1 = fig.add_subplot()
    # ax1.scatter(s.index, s.values,color='red')
    # plt.grid()
    #
    # plt.show()

    s.to_csv("分布"+filenmae2+".csv", encoding="utf_8_sig")

    # # 4.5
    # 可视化
    # topic.visualize_lda()

     #存储与导入lda模型
    # topic = Topic(cwd=os.getcwd())
    # topic.load_dictionary(dictpath='output/dictionary.dict')
    # topic.create_corpus(documents=documents)
    # topic.load_lda_model(modelpath='output/model/lda.model')




