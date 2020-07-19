import jieba
from os import path
import pandas as pd
from tqdm import tqdm
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import os
os.chdir('C:\\Users\\Simmons\\PycharmProjects\\cpc')

data_cpc = pd.read_excel('./data/中共全国代表大会文本数据库.xlsx', encoding = 'gbk')

stop = open('./data/stop_word.txt', 'r+', encoding='utf-8')
stopword = stop.read().split("\n")


# 输入一个str，返回词频dataframe
def word_count(s=''):
    jieba.load_userdict('./data/userdict.txt')
    tl = jieba.cut(s, cut_all=False)
    word_list = []
    for key in tqdm(tl):
        if key not in stopword:
            word_list.append(key)
        else:
            pass
    word_list = [ x for x in word_list if x != '' ]
    total_num = len(word_list)
    textdf = pd.DataFrame(columns=[ 'text' ])
    textdf[ 'text' ] = word_list
    count = textdf[ 'text' ].value_counts()
    count = count.reset_index()
    count[ 'total_num' ] = total_num
    return count


data_cpc['附加'] = data_cpc['附加'].fillna('')

data_cpc['text_1'] = data_cpc['text'] + data_cpc['附加']


def count_out(tag='', df=pd.DataFrame()):
    xlsx = pd.ExcelWriter('./data_out/{0}.xlsx'.format(tag))
    df_tag = df.loc[df['tag'] == tag, :]
    for i in tqdm(df_tag.index):
        df_count = word_count(str(df_tag.loc[i, 'text_1']))
        df_count['会议'] = str(df_tag.loc[i, '会议2'])
        df_count[ 'time' ] = str(df_tag.loc[ i, '时间' ])
        name = str(df_tag.loc[i, 'name'])
        if len(name) > 31:
            name = name[0:30]
        if ']' in name:
            name = name.split(']')[1]
        else:
            pass
        df_count.to_excel(xlsx, sheet_name='{0}'.format(name), encoding='gbk')
    xlsx.save()


count_out(tag = '公报', df = data_cpc)
count_out(tag = '报告', df = data_cpc)
count_out(tag = '决议', df = data_cpc)
count_out(tag = '社论', df = data_cpc)