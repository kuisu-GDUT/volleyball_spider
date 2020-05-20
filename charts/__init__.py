
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
fm.FontProperties(fname='font/SimHei.ttf')

# 数据信息
# Surname(姓)
# Name(名)
# Team(队伍)
# Played Matches(参加比赛)
# Played Sets(局数)
# Total Points(总分数)
# Break Points(防反)
# W-L(净得分)
# Serve Err(发球失误)
# Serve Ex(发球效果较好)
# Serve HP(发球破攻)
# Serve Minus(发球效果一般)
# Serve Plus(发球效果很好)
# Serve Win(发球得分)
# Rec Err(一传失误)
# Rec Ex(一传不到位)
# Rec HP(一传不到位)
# Rec Minus(一传效果不佳)
# Rec Plus(一传到位)
# Rec Win(一传非常到位)
# Rec Pos%(起球率)
# Rec Perf%(到位率)
# Spike Err(进攻失误)
# Spike Ex(进攻被拦回)
# Spike HP(进攻被拦死)
# Spike Minus(进攻效果不佳)
# Spike Plus(进攻效果较好)
# Spike Win(进攻得分)
# Spike Pos%(成功率)
# Block Err(拦网失误)
# Block Ex(拦网未拦死)
# Block HP(触网)
# Block Minus(拦网效果不佳)
# Block Plus(拦网效果较好)
# Block Win(拦网得分)
def data_analysis():

    # 找到运动员的所有数据信息
    # csv_list=glob.glob('data/player_data_*.csv')
    # data_list=[]
    # for csv_file in csv_list:
    #     temp_data=pd.read_csv(csv_file)
    #     temp_data.set_index('PlayerID',inplace=True)
    #     data_list.append(temp_data)
    # for data in data_list:
    #     # print(data.index)
    #     Series(data['SpikeErr'],index=data.index)
    #     gen_spike_bar(data)


    gen_spike_bar(pd.read_csv('data/player_data_2019_第四阶段.csv',encoding='gbk'),'2019总诀赛进攻排名前八进攻数据')
    gen_spike_bar(pd.read_csv('data/player_data_2018_第四阶段决赛.csv',encoding='gbk'),'2018总诀赛进攻排名前八进攻数据')

'''
队员进攻柱状图绘制
'''
def gen_spike_bar(data,title):
    data=data[data['SpikePos']!= '.'].sort_values(by='SpikePos',ascending=False)[0:8]
    # 获取队员的名称
    data['FullName']=data['Surname']+data['Name']
    # x轴为名称
    full_name=data['FullName']
    # 进攻失误
    spike_err=data['SpikeErr']
    # 进攻效果不佳
    spike_minus=data['SpikeMinus']
    # 进攻效果较好
    spike_plus=data['SpikePlus']
    # 进攻得分
    spike_win=data['SpikeWin']
    # 触网
    spike_hp=data['SpikeHP']
    # 进攻被拦回
    spike_ex=data['SpikeEx']
    plt.bar(full_name,spike_err,label='进攻失误',color='red')
    plt.bar(full_name,spike_minus,label='进攻效果不佳',color='orange')
    plt.bar(full_name,spike_plus,label='进攻效果较好')
    plt.bar(full_name,spike_win,label='进攻得分',color='green')
    plt.bar(full_name,spike_hp,label='触网')
    plt.bar(full_name,spike_ex,label='进攻被拦回')
    plt.legend()
    # 图片像素
    plt.rcParams['savefig.dpi'] = 300
    # 分辨率
    plt.rcParams['figure.dpi'] = 300
    # 尺寸
    plt.rcParams['figure.figsize'] = (15.0, 8.0)
    # 设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.xlabel('姓名')
    plt.ylabel('进攻数')
    plt.title(title)
    plt.show()

