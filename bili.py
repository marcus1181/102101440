import requests
from bs4 import BeautifulSoup
import re
import jieba
import wordcloud
from collections import Counter
import imageio
from openpyxl import Workbook,load_workbook

#定义请求头
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
#定义页数page和o来翻页
page=0
o=0
#存放视频bv号
list_ = []

#翻页提取视频bv号

while page<10:
    url = 'https://search.bilibili.com/all?keyword=%E6%97%A5%E6%9C%AC%E6%A0%B8%E6%B1%A1%E6%9F%93%E6%B0%B4%E6%8E%92%E6%B5%B7&from_source=webtop_search&spm_id_from=333.1007&search_source=3&page={0}&o={1}'.format(page,o)
    print(url)
    response=requests.get(url=url,headers=headers)
    text1=response.text
    html=re.findall(r'(BV.{10})',text1)
    list_.extend(html)
    page=page+1
    o=o+36
ll = []
for k in list_:
    if ll.count(k)==0:
        ll.append(k)
#输出爬取的视频数量
print('------------------------b站弹幕智能数据分析程序--------------------')
print('-------------------------获取关键词：日本和污染水排放的弹幕数据-------------')
print('--------------------------正在获取中  Loading......-------------------------')
print("爬取的视频数量：")
print(len(ll))
print("-------------生成日本核污染水排海弹幕.txt文件------------")
print("=============生成日本和污染水排海弹幕爬取.xlsx文件===========")

#获取前300个视频链接
for j in list_[:300]:
    link = "https://www.bilibili.com/video/{}/".format(j)
    response = requests.get(url=link, headers=headers)
    response.encoding = 'utf-8'
    html1 = response.text
#获取cid以此获得弹幕地址
    cid_ = re.search(r'"cid":(\d*),', html1)
    cid=cid_.group(1)
    link_danmu = "https://comment.bilibili.com/{}.xml".format(cid)
    response2 = requests.get(link_danmu)
    response2.encoding = 'utf-8'
    soup2 = BeautifulSoup(response2.text, 'xml')
    all_danmu = soup2.findAll("d")

    #print(all_danmu)
#将弹幕存入文件中
    for danmu in all_danmu:
        with open('日本核污染水排海弹幕.txt', 'a', newline='', encoding='utf-8-sig') as file:
            file.write(danmu.string)
            file.write("\n")
#生成表格
exce=Workbook()
sheet=exce.active
print(sheet.title)
sheet.title="b站弹幕搜集"
sheet["A1"]="编号"
sheet["B1"]="弹幕"
sheet["C1"]="出现次数"
exce.save("日本和污染水排海弹幕爬取.xlsx")
i=1
f = open('日本核污染水排海弹幕.txt','r',encoding= 'utf-8')
a = f.read()
list = a.split("\n")
for i in range(0,1000) :
    sheet.append([i+1,list[i],list.count(list[i])])
exce.save("日本和污染水排海弹幕爬取.xlsx")


#开始制作词云图
fl=open('日本核污染水排海弹幕.txt',"r", encoding='utf-8-sig')
text=fl.read()
text_string=text.split()
count=Counter(text_string)
sum=count.most_common(20)
print("综合排序前300的视频出现最多次数的弹幕前20是:")
print(sum)
#进行分词
jieba.setLogLevel(jieba.logging.INFO)
short=jieba.lcut(text)
cut_string=' '.join(short)
#设置词云图参数
pct=wordcloud.WordCloud(
    width=1000,
    height=000,
    scale=16,
    background_color='white',
    font_path='msyh.ttc',
    stopwords={'的','你','我们'},
)

pct.generate(cut_string)
pct.to_file('弹幕词云.png')







