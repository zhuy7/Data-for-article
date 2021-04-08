# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 16:17:23 2021

@author: Administrator
"""
"""
需要对事故后果进行量化
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:10:04 2021

@author: KieraLynn
"""

"""
参数说明
1、时间范围 两年期间8个Quaters
第1年Q1:1-68 Q2:69-132 Q3:133-195 Q4:196-262
第2年Q5:263-294 Q6:295-332 Q7:333-368 Q8:369-411
2、输入的原始数据
severity_threshold= 0.15#事故后果阈值
"""
import itertools
from clean_data import *
from Hierarchy_tree import *
import Trimming_Header_table
import csv
#severity_threshold= 0.15#事故后果阈值
tran_score = copy.deepcopy(datas)
severity=[]

def wtf():
    for i in range(1,412):
        tran = tran_score[i]
        death =tran['死亡']
        minor = tran['轻伤']
        severe =tran['重伤']
        cost = tran['经济损失']
        if death == 0 :
            if severe == 0:
                if 0<minor < 3 or 0<cost < 1 :
                    tran['score'] = 0.01
                elif minor ==0 and cost ==0:
                    tran['score'] = 0
                elif minor >= 3 or 1 <= cost < 5:
                     tran['score'] = 0.05
                elif 5 <= cost < 10:
                    tran['score'] = 0.1
            elif severe ==1:
                tran['score'] = 0.05
            elif severe > 1 :
                tran['score'] = 0.1

        elif death < 3 or 10 <= cost < 20:
            tran['score'] = 1
        elif death > 3:
            tran['score'] = 10
    tmp_ac = []
    for tran in  tran_score[1:412]:
        if tran['事件类型'] == '事故':
            tmp_ac.append(tran)
    tmp_ac.insert(0,'事故严重程度')
    for i in range(1,149):
        severity.append([])
    severity.insert(0,'事故严重程度')
    for i in range(1,len(tmp_ac)):
        severity[i].append(tmp_ac[i]['score'])
        severity[i].append(accidents[i])
wtf()
del tran_score
raw=[]
def mined_data(period):
    with open('./try.csv', 'r') as f:
        reader = csv.reader(f)
        #print(type(reader))
        for row in reader:
            period.append(row)
    for tran in period:
        if " " in tran :
            tran.remove(" ")
        if " " in tran :
            tran.remove(" ")
        if " " in tran :
            tran.remove(" ")
        if " " in tran :
            tran.remove(" ")
        else:
            pass
        if " " in tran :
            tran.remove(" ")
        else:
            pass
        tran.pop(len(tran)-1)
mined_data(raw)
score_of_mined =[]
sever_res=[]
def prunning():
    for i in range(len(raw)):
        score_of_mined.append([])
        score_of_mined[i].insert(0,raw[i])
        for j in range(1,len(severity)):
            set1 = set(severity[j][1])
            set2= set(raw[i])
            if set1 >= set2:
                score_of_mined[i].insert(0,severity[j][0])
    for i in range(0,len(score_of_mined)):
        sum_score =[]
        for item in score_of_mined[i]:
             if type(item) is not list:
                 sum_score.append(item)
        if sum(sum_score) > 0.07:
            sever_res.append(score_of_mined[i])
prunning()

def organize():
    for i in range(0,len(sever_res)):
        sum1 =[]
        for item in sever_res[i]:
            if type(item) is not list:
                sum1.append(item)
        sever_res[i].insert(0,sum(sum1))
        del sever_res[i][1:len(sever_res[i])-1]
organize()


def output_excel(data):
    output = open('data.xls','w',encoding='gbk')
    for i in range(len(data)):
        for j in range(len(data[i])):
             output.write(str(data[i][j]))  #write函数不能写int类型的参数，所以使用str()转化
             output.write('\t')  #相当于Tab一下，换一个单元格
        output.write('\n')    #写完一行立马换行
    output.close()
output_excel(sever_res)


