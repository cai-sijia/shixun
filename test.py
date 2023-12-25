import requests
import streamlit as st
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import csv
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from pyecharts.charts import WordCloud,Funnel,Line,Bar,Pie
from pyecharts.faker import Faker
from pyecharts.options import LabelOpts
import numpy as np
import seaborn as sns
import pandas as pd
from matplotlib.font_manager import FontProperties 
import matplotlib
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
    matplotlib.rcParams['font.family'] = 'SimHei'  # 设置为中文字体
    plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
    plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题
    plot_types = ("折线图","柱状图","饼状图" ,"散点图","词云图","漏斗图","蜘蛛图") # 选择绘制的图表种类 
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
    elif chart_type=='蜘蛛图':
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
   fig=plt.figure()
   plt.title("散点图")
   plt.scatter(word,number)
   st.pyplot(fig)
   


def cy(data):
    wc=WordCloud()
    wc.add(series_name="测试",data_pair=data)
    ste.st_pyecharts(wc)

def ld(word,number):
   wf = Funnel()
   wf.add('漏斗图',[list(z) for z in zip(word, number)])
   ste.st_pyecharts(wf)

def zz(word,number):
    n = len(number)
    angles = [i * 2 * math.pi / n for i in range(n)]
    angles.append(angles[0])
    number.append(number[0])
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, number)
    ax.fill(angles, number, alpha=0.3)
    ax.set_thetagrids([a * 180 / math.pi for a in angles[:-1]], word)
    ax.grid(True)
    ax.plot(angles, number, 'o', linewidth=2)
    ax.plot(angles, number, color='r', linewidth=2)
    st.pyplot(fig)

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
