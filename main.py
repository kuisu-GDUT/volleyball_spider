import charts
import scrap
base_url = 'http://cva-web.dataproject.com'


if __name__ == '__main__':
    # 爬取数据
    print('开始爬取2018年,女排比赛数据...')
    # scrap.data_scrap(base_url + '/CompetitionHome.aspx?ID=4',2018)
    print('开始爬取2019年,女排比赛数据...')
    # scrap.data_scrap(base_url + '/CompetitionHome.aspx?ID=37',2019)
    # 分析数据
    print('开始执行数据数据可视化...')
    charts.data_analysis()
    # 'http://cva-web.dataproject.com/CompetitionHome.aspx?ID=4'