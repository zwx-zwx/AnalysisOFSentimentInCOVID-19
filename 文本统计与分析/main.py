import csv
from collections import Counter
import jieba.posseg as psg
import numpy as np
import math
from pyecharts import options as opts
from pyecharts.charts import WordCloud


def split(parameter):
    stopword = []
    with open('data/stoplist.txt', 'r', encoding='GBK') as s:
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
    m = [i for i in k if len(i) > 1 or i == '🙏']  # 去长度为1的词(除了🙏)
    return np.array(m).tolist()


with open('data/stage1.csv', 'r', encoding='utf8') as data:  # 四个阶段分别打开
    t = [row for row in csv.DictReader(data)]


def WordCloud_base() -> WordCloud:
    all = ""
    for i in range(0, len(t)):
        all = all + t[i]['评论']  # 整个文本库
    all_words = split(all)
    all_wordcount = Counter(all_words)  # 文本库中的词频统计
    words = sorted(all_wordcount.items(), key=lambda d: d[1], reverse=True)[:30]
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 100], shape='circle')  # SymbolType.ROUND_RECT
            .set_global_opts(title_opts=opts.TitleOpts(title='第一阶段'))  # 四个阶段分别绘制
    )
    return c


def distribute():
    # 文本库统计
    all = ""
    for i in range(0, len(t)):
        for j in t[i]['评论'].split(','):
            all = all + j  # 整个文本库
    all_words = split(all)
    num_of_all = len(all_words)  # 文本库中词的总频数
    all_wordcount = Counter(all_words)  # 文本库中的词频统计

    # 导入心态词典
    mentality_dict = {'事不关己': ["嘲笑", "掉以轻心", "幸灾乐祸", "小题大做", "侥幸", "无所谓"],
                      '困惑质疑': ["请问", "瞒报", "怀疑", "造谣", "没想到", "不信", "不好", "不配", "没用", "为啥",
                               "管管", "胡说八道", "怎么回事"],
                      '痛苦悲伤': ["困难", "黑暗", "好不容易", "太不容易", "来之不易", "功亏一篑", "心疼", "寒冬",
                               "默哀", "哀悼", "委屈", "不容乐观", "呜呜", "失望", "无奈", "难受", "痛心", "崩溃",
                               "难过", "倒霉", "内疚", "绝望", "遭殃"],
                      '愤懑不平': ["气死我了", "发国难财", "跟风", "抱怨", "暴乱", "哄抬物价", "害人害己", "添麻烦", "愤怒",
                               "不肖子孙", "欺上瞒下", "秋后算账", "很烦", "不要脸"],
                      '焦虑恐慌': ["买不到", "救救", "求求", "麻烦", "紧张", "恐慌", "没货", "可怕", "遥遥无期", "恐怖",
                               "吓人", "没谱", "害怕", "着急", "赶紧", "告急", "发抖", "慌张", "无能为力", "人心惶惶",
                               "恐惧", "不堪设想", "心慌", "咋办"],
                      '担忧关切': ["严惩", "严防", "严控", "重视", "警惕", "严查", "加油", "支持", "挺住", "平安", "捐款",
                               "捐赠", "理解", "尊重", "珍惜", "请求", "强烈建议", "呼吁", "恳请", "对不起", "保重", "担心",
                               "担忧", "强烈要求", "揪心"],
                      '美好期盼': ["希望", "好好", "早日", "春暖花开", "春天", "期待", "清零", "健康", "胜利", "打赢", "做好",
                               "恢复", "早日康复", "羡慕", "无恙", "必胜", "好转", "安好", "更好", "🙏"],
                      '感动赞美': ["辛苦", "感谢", "温暖", "善良", "牺牲", "最美", "强大", "付出", "喜欢", "厉害", "可爱", "感恩",
                               "值得", "感动", "奉献", "骄傲", "不错", "漂亮", "美好", "了不起", "无私", "真好", "有用", "顶上去",
                               "很棒", "好样", "做得好", "好评", "致敬"],
                      '轻松愉悦': ["太好了", "放松", "很好", "舒服", "恭喜", "终于", "哈哈哈", "没事", "幸福", "放心", "快乐", "哈哈哈哈",
                               "开心", "自信", "好开心", "安心"],
                      '坚定信任': ["努力", "八方支援", "万众一心", "共渡难关", "坚强", "援助", "团结", "配合", "支援", "担当", "负责",
                               "奋斗", "风雨同舟", "稳住", "严防死守", "坚守", "勇敢", "精诚合作", "奋战", "共度难关", "守护", "团结起来",
                               "团结一心", "一方有难"]}

    # 初始化心态分布表
    distribution_dict = {'事不关己': 0, '困惑质疑': 0, '痛苦悲伤': 0, '愤懑不平': 0, '焦虑恐慌': 0, '担忧关切': 0, '美好期盼': 0, '感动赞美': 0,
                         '轻松愉悦': 0, '坚定信任': 0}

    # 每一条评论为单位计算心态权重
    for i in range(0, len(t)):
        for j in t[i]['评论'].split(','):
            TF = {}
            IWF = {}
            TF_IWF = {}
            wordcount = Counter(split(j))  # 当前文本中的词频统计
            total = 0  # 当前文本中词的总频数
            for value in wordcount.values():  # 值相加得总频数
                total = total + value
            for key in wordcount.keys():
                tf = wordcount[key] / total  # 计算tf,即该词在文本中出现的频率
                TF[key] = tf
                num_of_word = all_wordcount[key]  # 该词在文本库中出现的总频数
                iwf = math.log10(num_of_all / (num_of_word + 1))  # 计算iwf
                IWF[key] = iwf
                TF_IWF[key] = tf * iwf
            for key in TF_IWF.keys():
                for mentality in mentality_dict.keys():
                    if mentality_dict[mentality].__contains__(key):
                        distribution_dict[mentality] += TF_IWF[key]

    # 计算每种心态的占比
    total_weight = 0
    for value in distribution_dict.values():
        total_weight += value
    for key in distribution_dict.keys():  # 重新赋值(百分数)
        distribution_dict[key] = (distribution_dict[key] / total_weight) * 100
    return sorted(distribution_dict.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    WordCloud_base().render('第一阶段.html')  # 四个阶段分别绘制
    with open('data/distribute.csv', 'a', newline="") as wr:
        writer = csv.writer(wr)
        writer.writerow([distribute()])

