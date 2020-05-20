

from pandas import Series,DataFrame
import requests
import re
import time
import tldextract
from bs4 import BeautifulSoup
import os
import csv
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import glob



'''
  获取html 源码
'''


def get_bs4(url):
    return html2bs4(get_html(url))


def get_html(url):
    return requests.get(url).text


def html2bs4(html):
    if html == None:
        return
    return BeautifulSoup(html, 'html.parser')

'''
    通过html获取队伍数据信息
    1. 先获取阶段信息
    2. 获取回合信息
    3. 获取比赛信息
'''


def get_competition_data(url):
    '''
    输入url, 获取该网页上的数据线信息
    :param url:
    :return: ['阶段','组别','轮数','时间','地点','组A','A组分数','组B','B组分数','裁判']结果
    '''
    bs4 = get_bs4(url)
    result = []
    # os.makedirs('html/CompetitionMatches',0o777,True)
    # with open('html/CompetitionMatches/'+name+'.html','w') as html:
    #     html.write(bs4.prettify())
    # 找到页面中的数据
    contentmain = bs4.find_all(name='div', id='Content_Main_RPL_Master')
    # 获取阶段名称
    stage = bs4.h3.string.strip()#'第一阶段精英赛'
    # print('stage name :' + stage)
    # print(type(contentmain))
    temp = html2bs4(str(contentmain[0]))#将html转为bs树, 方便检索.
    # 找到组的信息
    group_content = html2bs4(str(temp.find('div', id='ctl00_Content_Main_RadTabStrip1')))
    group_set = group_content.find_all('span', class_='rtsTxt')#[<span class="rtsTxt">精英赛 - A组</span>, <span class="rtsTxt">精英赛 - B组</span>]
    # for group in group_set:
    #     print(group.string.strip())

    # 找到阶段数据的主体
    content_set = temp.find_all(name='div', attrs={'id': re.compile('^Content_Main_[0-9]{0,}$')})
    index = 0
    #todo 数据集合--> 查找printableArea块--> 再查找_userControl_RADLIST_Legs_ctrl0_RADLIST_Matches_ctrl-->获取每一行数据信息
    for content in content_set:
        # 找到每轮数据的集合
        content_temp = html2bs4(str(content))
        # 获取当前元素的id
        # print(content_temp.div['id'])
        content_id_temp = content_temp.div['id']# 'Content_Main_4'
        # content_temp.find('div',attrs={'id':'printableArea'})
        bout_set = html2bs4(str(content_temp.find('div', attrs={'id': 'printableArea'}))).div.find_all('div',
                                                                                                       recursive=False)
        for bout in bout_set:
            temp_bout = html2bs4(str(bout))
            h3 = temp_bout.h3
            if h3 == None:
                continue
            bout_name = h3.string.strip()
            content_set_temp = temp_bout.find_all('div', attrs={'id': re.compile(
                '^ctl00_' + content_id_temp + '_userControl_RADLIST_Legs_ctrl0_RADLIST_Matches_ctrl[0-9]_MatchRow$')})
            for content_item in content_set_temp:
                # print(content_item)
                #                 html2bs4(str(content_item)).find_all(text=re.compile('^\d{4}/\d{1,2}/\d{1,2} - \d{1,2}:\d{1,2}$'))
                #                 获取到每一行的数据信息
                # todo '阶段','组别','轮数','时间','地点','组A','A组分数','组B','B组分数','裁判'
                temp_com = Competittion()
                # 阶段
                temp_com.stage = stage
                # 组别
                temp_com.group = group_set[index].string.strip()
                # 轮数
                temp_com.bout = bout_name
                content_item_temp = html2bs4(str(content_item))
                content_row_set = content_item_temp.find_all('div', class_="Calendar_DIV_Column")
                # temp_com.date = content_row_set[1].find_all('p')[0].span.string.strip()
                # temp_com.address = content_row_set[1].find_all('p')[1].span.string.strip()
                # temp_com.team_a = content_row_set[4].find_all('p')[0].span.b.string.strip()
                # temp_com.team_a_score = content_row_set[6].find_all('span')[0].b.string.strip()
                # temp_com.team_b_score = content_row_set[6].find_all('span')[2].b.string.strip()
                # temp_com.team_b = content_row_set[8].span.string.strip()
                # temp_com.referee = content_row_set[9].find_all('span')[0].string.strip() + '|' + \
                #                    content_row_set[9].find_all('span')[1].string.strip()
                temp_com.date = content_row_set[1].find_all(text=re.compile(r'\S'))[0].string.strip()
                temp_com.address = content_row_set[1].find_all(text=re.compile(r'\S'))[1].string.strip()
                temp_com.team_a = content_row_set[4].find_all(text=re.compile(r'\S'))[0].string.strip()
                temp_com.team_a_score = content_row_set[6].find_all(text=re.compile(r'\S'))[0].string.strip()
                temp_com.team_b_score = content_row_set[6].find_all(text=re.compile(r'\S'))[2].string.strip()
                temp_com.team_b = content_row_set[8].find_all(text=re.compile(r'\S'))[0].string.strip()
                temp_com.referee = content_row_set[9].find_all(text=re.compile(r'\S'))[0].string.strip() + '|' + \
                                   content_row_set[9].find_all(text=re.compile(r'\S'))[1].string.strip()
                result.append(temp_com)
                # print(str(temp_com))
        index = index + 1
    return result


# '阶段','组别','轮数','时间','地点','组A','A组分数','组B','B组分数','裁判'
class Competittion:
    stage = None
    group = None
    bout = None
    date = None
    address = None
    team_a = None
    team_a_score = None
    team_b = None
    team_b_score = None
    referee = None


'''
中国女子超级排球联赛地址:
http://cva-web.dataproject.com

中国女子超级排球联赛包含以下页面
 1. CompetitionHome.aspx 首页
 2. CompetitionMatches.aspx 队伍比赛页面,包含队伍的比赛记录
 3. CompetitionStandings.aspx 成绩公告页面
 4. Statistics.aspx 数据统计页面
 5. CompetitionTeamSearch.aspx 球队信息页面
 6. CompetitionPlayerSearch.aspx 球员信息页面
 7. CompetitionTeamDetails.aspx 球队详细信息页面
 8. PlayerDetails.aspx 球员详细页面
'''
def data_scrap(url,year):
    base_url = 'http://cva-web.dataproject.com'
    soup = get_bs4(url)
    links=[]
    links.extend([a.get('href','/') for a in soup.find_all('a')])#获得所有的链接
    competition_list = [
        ['stage', 'group', 'bout', 'date', 'address', 'team_a', 'team_a_score', 'team_b', 'team_b_score', 'referee']]
    for link in links:
        splits = link.split('?')#'CompetitionHome.aspx?ID=21'
        page = splits[0]#判断是否为比赛信息
        # 比赛信息
        # 需要保存比赛信息到csv文件中去
        # 文件格式的定义:
        # 阶段,组别,轮数,时间,地点,组A,比分,组B,裁判
        if page == 'CompetitionMatches.aspx':#比赛信息(ID,PID)
            param = splits[1]#ID=21
            data = get_competition_data(base_url + '/' + link)#获取队伍比赛数据
            params=param.split('&')
            comp_id=params[0].split('=')[1]
            phase_id=params[1].split('=')[1]
            stage=data[1].stage
            for d in data:#data为迭代器, 需遍历添加到列表中
                competition_list.append(
                    [d.stage, d.group, d.bout, d.date, d.address, d.team_a, d.team_a_score, d.team_b, d.team_b_score,
                     d.referee])
            # 爬取该阶段所有队员的数据(第一阶段精英赛, 第二阶段,...
            scrap_all_player_data(comp_id,phase_id,year,stage)
        elif 'CompetitionStandings.aspx' == page:
            pass
        elif 'Statistics.aspx' == page:
            pass
        elif 'CompetitionTeamSearch.aspx' == page:
            pass
    # 写入队伍比赛数据
    with open('data/competition_matches_'+str(year)+'.csv', 'w') as csvfile:
        cfw = csv.writer(csvfile)
        for temp in competition_list:
            cfw.writerow(temp)


'''
爬取队员数据
'''

def scrap_all_player_data(comp_id, phase_id,year,stage):
    # 先获取当前页面的数量
    get_count_data={"filterExpressions":[],
                    "compID":str(comp_id),
                    "phaseID":str(phase_id),
                    "playerSearchByName":""}
    count_data = requests.post('http://cva-web.dataproject.com/Statistics_AllPlayers.aspx/GetCount',
                                json=get_count_data)
    count_dict = json.loads(count_data.text)#{"d":186}
    count=count_dict['d']

    # 请求参数
    request_data = {
        "startIndex": 0,
        "maximumRows": count,#一次全部获取
        "sortExpressions": "",
        "filterExpressions": [],
        "compID": str(comp_id),
        "phaseID": str(phase_id),
        "playerSearchByName": ""
    }
    player_data = requests.post('http://cva-web.dataproject.com/Statistics_AllPlayers.aspx/GetData',
                                json=request_data)
    # 起始索引值
    csv_column_list=['RankingTypeID', 'PointsTot_ForAllPlayerStats', 'SpikePerf', 'SpikePos', 'RecPos', 'RecPerf', 'PointsW_P', 'Libero', 'SpikeTot', 'RecTot', 'PlayedMatches', 'PlayedSet', 'SpikeWin_MatchWin', 'SpikeWin_MatchLose', 'BlockWin_MatchWin', 'BlockWin_MatchLose', 'ServeWin_MatchWin', 'ServeWin_MatchLose', 'RecEffPerc', 'RecWinPerc', 'ServeWinMatch', 'ServeWinSet', 'BlockWinSet', 'SpikerEff', 'SpikerPos', 'SpikerPerSet', 'PointsTot', 'MatchName', 'PointsPerMatch', 'PointsPerSet', 'PlayerSetData', 'PlayerMatchID', 'ChampionshipMatchID', 'ChampionshipID', 'TeamID', 'PlayerID', 'PlayedSets', 'Points', 'SideOut', 'ServeErr', 'ServeWin', 'ServeMinus', 'ServePlus', 'ServeHP', 'ServeEx', 'RecErr', 'RecWin', 'RecMinus', 'RecPlus', 'RecHP', 'RecEx', 'SpikeErr', 'SpikeWin', 'SpikeMinus', 'SpikePlus', 'SpikeHP', 'SpikeEx', 'BlockErr', 'BlockWin', 'BlockMinus', 'BlockPlus', 'BlockHP', 'BlockEx', 'PositionID', 'Captain', 'Number', 'Vote', 'Surname', 'Name', 'Team']
    csv_data_list=[csv_column_list]
    dict_data = json.loads(player_data.text)
    for d in dict_data['d']:
        temp = []
        for column in csv_column_list:
            temp.append(d[column])
        csv_data_list.append(temp)
    #     将数据写入文件
    with open('data/player_data_'+str(year)+'_'+str(stage)+'.csv',mode='w') as csvfile:
        cfw=csv.writer(csvfile)
        for d in csv_data_list:
            cfw.writerow(d)



'''
采集单个队员的数据信息
'''
def scrap_single_player_data(comp_id,phase_id,player_id,path='data/player'):
    if None == player_id:
        return
    request_data={"compId":str(comp_id),"phaseId":str(phase_id),"playerSearchById":str(player_id)}
    print(json.dumps(request_data))
    # 获取到队员的总数据
    response=requests.post('http://cva-web.dataproject.com/Statistics_AllPlayers.aspx/GetDataById',json=request_data)
    print(response.text)
    url='http://cva-web.dataproject.com/Statistics_AllPlayers.aspx?ID='+str(comp_id)+'&PID='+str(phase_id)+'&Player='+str(player_id)
    # 获取到队员的个人网页并解析出来个人的比赛数据
    single_player_html=requests.get(url)
    with open('html/single_player.html','w') as html:
        html.write(single_player_html.text)