import requests
import streamlit as st
from bs4 import BeautifulSoup
import jieba
from pyecharts.charts import WordCloud,Funnel,Line,Bar,Pie,Scatter,Radar
from pyecharts.faker import Faker
from pyecharts.options import LabelOpts
import streamlit_echarts as ste
from pyecharts import options as opts
import re

def index_soup(soup):
    content=soup.find("body")
    doc=remove_html_tags(content.text)
    doc1=doc.replace(" ","")
    doc2=remove_punctuation(doc1)
    # 使用jieba进行分词
    tokens = jieba.lcut(doc2)
    counts = {}
    for word in tokens:
        if len(word) == 1: #长度为1的话，不储存
            continue
        else:   
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
     # 输出词频最高的20个词
    items.sort(key=lambda x: x[1], reverse=True)
    word=[key for key, value in items[:20:]]
    number= [value for key, value in items[:20:]]
    plot_types = ("折线图","柱状图","饼状图" ,"散点图","词云图","漏斗图","雷达图") # 选择绘制的图表种类 
    chart_type = st.sidebar.selectbox("选择图表类型：", plot_types)
    if chart_type=='折线图':
        zhexian(word,number)
    elif chart_type=='柱状图':
        zx(word,number)
    elif chart_type=='饼状图':
        bz(word,number)
    elif chart_type=='散点图':
        sd(word,number)
    elif chart_type=='词云图':
        cy(items)
    elif chart_type=='漏斗图':
        ld(word,number)
    elif chart_type=='雷达图':
        zz(word,number)
    select_option=("全部词频的统计","前二十的词频","过滤后低频词(次数小于等于5)")
    selected_option=st.sidebar.selectbox("展示",select_option)
    with st.container():     
        st.subheader(f"显示:  {selected_option}")     
        st.write("")
    if selected_option=='前二十的词频':
        for i in range(20): 
            word, count = items[i]
            st.write(f"{word} 出现的次数: {count}")
    elif selected_option=='全部词频的统计':
        for i in range(len(items)): 
            word, count = items[i]
            st.write(f"{word} 出现的次数: {count}")
    elif selected_option=='过滤后低频词(次数小于等于5)':
        for i in range(len(items)): 
            word, count = items[i]
            if int(count)>5:
                st.write(f"{word} 出现的次数: {count}")
            else:
                continue

def zhexian(word,number):
    line_chart = Line()
    # 添加x轴坐标
    line_chart.add_xaxis(word)
    # 添加y轴坐标，不显示数据
    line_chart.add_yaxis("", number, label_opts=opts.LabelOpts(is_show=False))
    # 设置全局选项，包括标题等
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
    ste.st_pyecharts(line_chart)

def zx(word,number):
    bar = Bar()
    #添加x轴数据
    bar.add_xaxis(word)
    #添加y轴数据
    #通过使用label_opts=LabelOpts(position='right')使数值标签显示在柱状图的右侧
    bar.add_yaxis('',number,label_opts=LabelOpts(position='right'))
    #通过使用reversal_axis()函数反转x，y轴
    bar.reversal_axis()
    #绘制柱状图
    ste.st_pyecharts(bar)

def bz(word,number):
    pie = Pie()
    pie.add('',[list(z) for z in zip(word,number)])
    ste.st_pyecharts(pie)

def sd(word,number):
   sca = Scatter()
   sca.add_xaxis(word)
   sca.add_yaxis("散点图",number)
   ste.st_pyecharts(sca)
   

def cy(data):
    wc=WordCloud()
    wc.add(series_name="测试",data_pair=data)
    ste.st_pyecharts(wc)

def ld(word,number):
   wf = Funnel()
   wf.add('漏斗图',[list(z) for z in zip(word, number)])
   ste.st_pyecharts(wf)

def zz(word,number):
   radar = Radar()
   radar.add_schema(
       schema=[opts.RadarIndicatorItem(name=str(i), max_=20) for i in word]      
)
   radar.add('',[number])
   radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
   radar.set_global_opts(title_opts=opts.TitleOpts('雷达图'))
   radar.render_notebook()
   ste.st_pyecharts(radar)

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
def remove_punctuation(text): # 使用正则表达式匹配所有的标点符号，并替换为空字符
    return re.sub(r'[^\w\s]', '', text)

url=st.text_input("请输入网页地址")
if url!="":
    r=requests.get(url)
    r.encoding='utf-8'
    if r.status_code!=200:
        raise Exception()
    html_doc=r.text
    soup=BeautifulSoup(html_doc,"html.parser")
    title=soup.title.string
    st.write("网页标题是：",title)
    index_soup(soup)
else:
    st.write("网址未输入")
