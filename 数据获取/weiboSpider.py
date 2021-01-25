"""
    python实现的微博爬虫，
    实现功能：根据一个微博ID 爬取该用户所有微博、基本信息以及评论
    输入：微博ID
    输出：一个json文件，文件名“name.json”
    文件内容： 该用户的微博标题，评论数、点赞数等

    微博接口：http://m.weibo.cn 即微博手机端
    存在问题：
        1. 没有cookie的条件下可以访问该用户至多2000条微博
        2. 由于微博的反爬机制，单个cookie不能过于频繁的访问服务器 --> cookie池
        3. cookie会在一段时间后更新 --> 模拟登录获得cookie
        4. 访问限制过高，约少于50秒访问一个页面 且 时间间隔一致 将被封号一段时间:(
    要点：
        1. 请求头要保存Cookie
        2. request频率不宜过高
        3. cookie会在一段时间后改变导致得不到需要的返回
    技术要领：
        1. 使用chrome开发者工具 掌握基本的网页的结构
        2. urllib.request 库的使用
        3. json模块的使用
        4. pyQuery 对得到的文本进行解析
        5. 服务器反爬机制 以及 对应的反反爬策略
"""

# coding=utf-8
import urllib.request
import json
from pyquery import PyQuery as pq
import calendar
import random
import time

# 接口
# 定义要爬取的微博大V的微博ID 和 昵称
id = '2028810631'

# 设置代理IP
proxy_addr=["196.168.0.1",
            "175.43.58.49:9999",
            "118.24.128.46:1080",
            "49.89.103.19:9999",
            "118.24.127.144:1080",
            "58.253.157.193:9999",
            "183.166.21.31:9999",
            "220.249.149.253:9999",
            "183.166.96.227:9999",
            "175.43.56.3:9999",
            "27.43.187.232:9999",
            "222.189.191.207:9999",
            "223.242.224.155:9999",
            "58.253.159.52:9999",
            "49.89.103.196:9999",
            "118.24.172.149:1080",
            "60.167.134.37:8888",
            "183.166.111.22:9999",
            "175.42.68.77:9999",
            "183.166.103.150:9999",
            "222.189.190.159:9999"]

# 收集到的常用Header
my_headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]



headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}


# 定义页面打开函数
def use_proxy(url,proxy_addr):
    req=urllib.request.Request(url,headers=headers)
    # req.add_header('User-Agent', random.choice(my_headers))
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')
    req.add_header('Cookie','WEIBOCN_FROM=1110006030; SUB=_2A25ND4lsDeRhGeFM7FoZ-C7JzTiIHXVu8xckrDV6PUJbkdAKLUXbkW1NQKQCsTOB-BJjOU7wsWx5eyPBfARGUyWf; _T_WM=20963664447; MLOGIN=1; XSRF-TOKEN=fbf2a5; M_WEIBOCN_PARAMS=oid%3D4596578541637430%26lfid%3D102803%26luicode%3D20000174%26uicode%3D20000174')
    # req.add_header('referer','https://m.weibo.cn/login?phone=13007527283&key=2NjdgC-ozAARy3UoU-GMr7Wlk3ZSjbksnDXB3YV9yZWdfbG9naW4.&loginScene=102003&backURL=https%3A%2F%2Fm.weibo.cn%2F')
    proxy=urllib.request.ProxyHandler({'http':random.choice(proxy_addr)})
    opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    data=urllib.request.urlopen(req).read().decode('utf-8','ignore')
    return data


# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
      if(data.get('tab_type')=='weibo'):
        containerid=data.get('containerid')
    return containerid


# 获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
    data=use_proxy(url,proxy_addr)
    content=json.loads(data).get('data')
    profile_image_url=content.get('userInfo').get('profile_image_url')
    description=content.get('userInfo').get('description')
    profile_url=content.get('userInfo').get('profile_url')
    verified=content.get('userInfo').get('verified')
    guanzhu=content.get('userInfo').get('follow_count')
    name=content.get('userInfo').get('screen_name')
    fensi=content.get('userInfo').get('followers_count')
    gender=content.get('userInfo').get('gender')
    urank=content.get('userInfo').get('urank')
    print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")
    return name

# 判断信息的时间段
def getStage(time):
    time=time.split()
    year = int(time[5])
    month = list(calendar.month_abbr).index(time[1])
    day = int(time[2])
    print("y-m-d:{}--{}--{}".format(year,month, day))
    if year==2019:
        if month==12 and day>8:
            return 1
    elif year==2020:
        if month==1:
            if day<=22:
                return 1
            elif day>=23:
                return 2
        elif month==2:
            if day<=7:
                return 2
            elif day>=10 and day<=13:
                return 3
        elif month>=3 and month<=6:
            if month==3 and day>=10:
                return 4
            elif month==6 and day<=15:
                return 4
            elif month!=6:
                return 4
    return 0


def getDate(time):
    time = time.split()
    year = time[5]
    month = str(list(calendar.month_abbr).index(time[1]))
    day = time[2]
    return year+month+day

# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id,file,bp):
    List = []
    i=bp
    begin = ''
    end = '1726918143'
    while begin!=end:
        url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id
        weibo_url='https://m.weibo.cn/api/container/getIndex?type=uid&value='+id+'&containerid='+get_containerid(url)+'&page='+str(i)
        print(weibo_url)
        try:
            data=use_proxy(weibo_url,proxy_addr)
            content=json.loads(data).get('data')
            cards=content.get('cards')
            if len(cards)>0 :
                for j in range(len(cards)):
                    print("-----正在爬取第"+str(i)+"页，第"+str(j)+"条微博------")
                    card_type=cards[j].get('card_type')
                    if(card_type==9):
                        mblog=cards[j].get('mblog')
                        attitudes_count=mblog.get('attitudes_count')
                        comments_count=mblog.get('comments_count')
                        created_at=mblog.get('created_at') # 创建时间
                        reposts_count=mblog.get('reposts_count')
                        scheme=cards[j].get('scheme')
                        ids=mblog.get('id')
                        # text=pq(mblog.get('text')).text().replace('\n','') # 文本内容
                        begin = getDate(created_at)
                        stage = getStage(created_at)
                        # 非需要的时间段，舍弃
                        if stage == 0:
                            print("stage0，前往下一页")
                            break
                        elif stage==3:
                            print("stage3 + 1")
                        elif stage==2:
                            print("stage2 + 1")
                        elif stage==1:
                            print("stage1 + 1")

                        dic = {
                            '微博地址:': scheme,
                            '发布时间:': created_at,
                            '微博标题:': get_detail(ids),
                            # '微博内容' : text,
                            '点赞数:': attitudes_count,
                            '评论数': comments_count,
                            '转发数': reposts_count,
                            '评论':get_comment(ids)
                        }
                        List.append(dic)
                        with open(file + str(stage) + ".json", 'w',encoding='utf-8') as fh:
                            fh.write(json.dumps(List, indent=2, ensure_ascii=False))
                        delay = 3.8 + 2.2 * random.random()
                        time.sleep(delay)
            else:
                print('nothing!!')
                break
            i+=1
        except Exception as e:
            get_weibo(id,file,i)
            print(e)


def get_comment(id):
    comments = []
    try:
        url='https://m.weibo.cn/comments/hotflow?id='+id+'&mid='+id+'&max_id_type=0'
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        datas = content.get('data')
        for i in range(0,11):
            if(i<len(datas)):
                comments.append(pq(datas[i].get('text')).text().replace('<span class=\"Text\".*?>.*?</span>', ''))
    except Exception as e:
        print(e)
        pass
    return comments

def get_detail(id):
    try:
        url='https://m.weibo.cn/statuses/extend?id='+id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        longTextContent = content.get('longTextContent')
        text=pq(longTextContent).text().replace('\n','')
    except Exception as e:
        print(e)
        pass
    return text

if __name__=="__main__":
    name = get_userInfo(id)
    file=name+"-stage"
    get_weibo(id,file,1757)