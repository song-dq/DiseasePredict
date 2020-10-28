import requests
import time
import json
from datetime import datetime
import urllib.request
import pandas as pd
import numpy as np
import os

def get_data(country_):
    url_ = 'https://gwpre.sina.cn/interface/news/wap/ncp_foreign.d.json?citycode=%s'%country_+'&callback=&_=%d'%int(time.time()*1000)
    request_ = urllib.request.Request(url=url_)
    response_ = urllib.request.urlopen(request_)
    text_ = response_.read()
    text_=text_[3:-5]
    data_ = json.loads(text_)['data']['historylist']
    #print(url_list2)
    #print(text_[0:3])
    #print(text_[-5:-1])
    #print(data)
    #print(len(text_))
    return data_

def get_data_cn():
    url_ = 'https://news.sina.com.cn/project/fymap/ncp2020_full_data.json?_=%d'%int(time.time()*1000)+'&callback='
    request_ = urllib.request.Request(url=url_)
    response_ = urllib.request.urlopen(request_)
    text_ = response_.read()
    text_=text_[13:-2]
    data_ = json.loads(text_)['data']['historylist']
    return data_

def get_province_country_list():
    url_ ='https://gwpre.sina.cn/interface/wap_api/feiyan/sinawap_get_area_tree.d.json?callback='
    pro_data = requests.get(url=url_).json()['data']['cities_cn']
    countries_data = requests.get(url=url_).json()['data']['countries']
    province_list = [elm_['e'] for elm_ in pro_data]
    country_list = [elm_['i'] for elm_ in countries_data]
    return province_list,country_list
def get_province_data(province_):
    url_list = 'https://gwpre.sina.cn/interface/news/ncp/data.d.json?mod=province&province=%s'%province+'&_=%d'%int(time.time()*1000)+'&callback='
    data_ = requests.get(url=url_list).json()['data']['historylist']
    return data_
########################## get province_list, country_list#####################
# logdir1 = 'd:/learn/code/python_code/epedemic/model_covid/data/province_list.json'
# logdir2 = 'd:/learn/code/python_code/epedemic/model_covid/data/country_list.json'
logdir1 = 'province_list.json'
logdir2 = 'country_list.json'

if os.path.exists(logdir1):
    print('province_list file exists!')
else:
    province_list,country_list=get_province_country_list()
    with open(logdir1,'w',encoding='utf-8') as f:
        f.write(json.dumps(province_list,ensure_ascii=False))
    with open(logdir2,'w',encoding='utf-8') as f:
        f.write(json.dumps(country_list,ensure_ascii=False))


#####################prepare CN data##########################################
country_ = 'CN'
logdir = ''.join(['%s' % country_, datetime.now().strftime("%y-%m-%d")])
if os.path.exists(logdir):
    print('CN file exists!')
else:
    data_ = get_data_cn()
    os.mkdir(logdir)
    with open(logdir+'/data.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data_,ensure_ascii=False))


#####################prepare USA data##########################################
country_ = 'SCUS0001'
logdir = ''.join(['%s'%country_, datetime.now().strftime("%y-%m-%d")])
if os.path.exists(logdir):
    print('USA file exists!')
else:
    data_ = get_data(country_)
    os.mkdir(logdir)
    with open(logdir+'/data.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data_,ensure_ascii=False))


##########################prepare province_data#####################################################

logdir = ''.join(['', datetime.now().strftime("%y-%m-%d")])
if os.path.exists(logdir):
    print('province_data file exists!')
else:
    os.mkdir(logdir)
    data_province=[]
    with open('province_list.json','r',encoding='utf-8') as f:
        province_list= json.load(f)
    for province in province_list:
        data_ = get_province_data(province)
        data_province.append(data_)
    with open(logdir+'/province_data.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data_province,ensure_ascii=False))