# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 13:53
# @Author  : ShenChong
# @Email   : 1536881202@qq.com
# @File    : crawler.py
# @Software: PyCharm Community Edition
import random
import re
import urllib2
import pandas as pd
import datetime
import requests
import json
# import execjs
import os
import time
from bs4 import BeautifulSoup
import xlwt
import xlrd
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Crawler_Fund_table:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        self.htmlpage=''#用来存储爬取的网页
        self.company_url_id=[]#用来存储基金公司的id
        self.company_url_rex='http://fund.10jqka.com.cn/market/xuangou/#orgid=(.*?)">.*?</a></em>'
        self.date=''#190513
        # http://fund.10jqka.com.cn/data/market/jjsx/?orgid[]=T000000015&count=500&key1=nowyear&sort=desc&zkl=0&page=1

        self.excel_head_dic={}#用来存储excel表格的属性 简称/拼音对应汉字

        self.row=0 #excel row
        self.matchid=""
        self.week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
    # 爬取html网页，并将内容复制给self.htmlpage
    def GetHtml(self,url):

        # # 代理IP
        # proxy_list = ['211.101.154.105','211.101.154.105','211.101.154.105','211.101.154.105','211.101.154.105','211.101.154.105','211.101.154.105','180.119.214.121:4557','125.123.16.24:4525','101.64.157.169:4528','114.230.184.121:4557','49.89.109.32:4576','117.92.129.202:4551','114.102.11.95:4516','180.116.22.199:4576' ]
        # # 接着在你使用的到urllib2的代码中，绑定某个IP，如下：
        # proxy = random.choice(proxy_list)
        # urlhandle = urllib2.ProxyHandler({'http': proxy})
        # opener = urllib2.build_opener(urlhandle)
        # urllib2.install_opener(opener)
        # # 正常使用urllib2
        # req = urllib2.Request(url, headers=self.headers)
        # self.htmlpage = urllib2.urlopen(req).read()

        self.htmlpage = ''
        req = urllib2.Request(url, headers=self.headers)
        response2 = urllib2.urlopen(req)
        self.htmlpage = response2.read()
        return self.htmlpage
    # 去除空格
    def RemoveSpace(self,content):
        p = re.compile('\s+')
        new = re.sub(p, '', content)
        return new

    # 将读取的str，或爬取的html(str)，输出到txt中
    def StrToTxt(self,name="html.txt"):
        f = open(name, 'w+')
        f.writelines(self.htmlpage)
        f.close()

    # 读取txt，到str中
    def TxtToStr(self, path):
        f = open(path, 'a+')
        str=f.read()
        f.close()
        return str

    def write_excel_mainpage(self, matchdata_json, items, row, sheet, date):
        for item  in items:
            # if date =='130206' and item.find('813737')>-1:
            #     print "hhh"
            if date =='130212' :
                print "hhh"
            list=item.split("^")
            sheet.write(row, 0, list[0])  # 比赛的id
            sheet.write(row, 1, list[2])  # 时间
            sheet.write(row, 2, list[6])  # 星期
            sheet.write(row, 3, list[7])  # 比赛类型
            sheet.write(row, 4, list[2])  # 月份
            sheet.write(row, 5, list[2])  # 时间点
            sheet.write(row, 6, matchdata_json[list[0]]['hrank'])  # 主队排名
            sheet.write(row, 7, list[8])  # 主队
            sheet.write(row, 8, str(matchdata_json[list[0]]["ascore"])+":"+str(matchdata_json[list[0]]["hscore"]))  # 比分
            sheet.write(row, 9, list[9])  # 客队
            sheet.write(row, 10, matchdata_json[list[0]]['grank'])  # 客队排名
            sheet.write(row, 11, str(matchdata_json[list[0]]["ahscore"])+":"+str(matchdata_json[list[0]]["hhscore"]))  # 半场比分
            if matchdata_json[list[0]]["sp"].has_key('jczq_xspf_gd'):
                sheet.write(row, 12, matchdata_json[list[0]]["sp"]['jczq_xspf_gd'])  # 竞彩赔率
            if matchdata_json[list[0]]["sp"].has_key('jczq_spf_gd'):
                sheet.write(row, 13, matchdata_json[list[0]]["sp"]['jczq_spf_gd'])  # 让球赔率
            rangqiutxt = test.TxtToStr('data\\rangqiu' + date +list[0]+ '.txt')  # 将磁盘的txt读取到str
            rangqiustrs = rangqiutxt.replace("'", '"')
            rangqiu_json = json.loads(rangqiustrs)  # dic
            jinqiutxt = test.TxtToStr('data\\jinqiu' + date + list[0] + '.txt')  # 将磁盘的txt读取到str
            jinqiustrs = jinqiutxt.replace("'", '"')
            jinqiu_json = json.loads(jinqiustrs)  # dic
            for li in rangqiu_json["result"]["asiaList"]:
                if li["companyName"]==u"澳门":
                    sheet.write(row, 14, float(li["firstHostOdds"].encode("utf-8"))/10000)  # 澳门初盘 主队赔率
                    sheet.write(row, 15, float(li["firstTape"].encode("utf-8"))/10000)  # 澳门初盘 让球
                    sheet.write(row, 16, float(li["firstAwayOdds"].encode("utf-8"))/10000)  # 澳门初盘 客队赔率
                    sheet.write(row, 17, float(li["hostOdds"].encode("utf-8"))/10000)  # 澳门终盘 主队赔率
                    sheet.write(row, 18, float(li["tape"].encode("utf-8"))/10000)  # 澳门终盘 让球
                    sheet.write(row, 19, float(li["awayOdds"].encode("utf-8"))/10000)  # 澳门终盘 客队赔率
                if li["companyName"] == u"Bet365":
                    sheet.write(row, 20, float(li["firstHostOdds"].encode("utf-8"))/10000)  # bet365初盘 主队赔率
                    sheet.write(row, 21, float(li["firstTape"].encode("utf-8"))/10000)  # bet365初盘 让球
                    sheet.write(row, 22, float(li["firstAwayOdds"].encode("utf-8"))/10000)  # bet365初盘 客队赔率
                    sheet.write(row, 23, float(li["hostOdds"].encode("utf-8"))/10000)  # bet365初盘 主队赔率
                    sheet.write(row, 24, float(li["tape"].encode("utf-8"))/10000)  # bet365初盘 让球
                    sheet.write(row, 25, float(li["awayOdds"].encode("utf-8"))/10000)  # bet365初盘 客队赔率
            for li in jinqiu_json["result"]["asiaList"]:
                if li["companyName"]==u"澳门":
                    sheet.write(row, 26, float(li["firstHostOdds"].encode("utf-8")) / 10000)  # 澳门初盘 主队赔率
                    sheet.write(row, 27,float(li["firstTape"].encode("utf-8")) / 10000)  # 澳门初盘 让球
                    sheet.write(row, 28, float(li["firstAwayOdds"].encode("utf-8")) / 10000)  # 澳门初盘 客队赔率
                    sheet.write(row, 29,float(li["hostOdds"].encode("utf-8")) / 10000)  # 澳门终盘 主队赔率
                    sheet.write(row, 30,float(li["tape"].encode("utf-8")) / 10000)  # 澳门终盘 让球
                    sheet.write(row, 31,float(li["awayOdds"].encode("utf-8")) / 10000)  # 澳门终盘 客队赔率
                if li["companyName"] == u"Bet365":
                    sheet.write(row, 32, float(li["firstHostOdds"].encode("utf-8")) / 10000)  # bet365初盘 主队赔率
                    sheet.write(row, 33, float(li["firstTape"].encode("utf-8")) / 10000)  # bet365初盘 让球
                    sheet.write(row, 34, float(li["firstAwayOdds"].encode("utf-8")) / 10000)  # bet365初盘 客队赔率
                    sheet.write(row, 35, float(li["hostOdds"].encode("utf-8")) / 10000)  # bet365初盘 主队赔率
                    sheet.write(row, 36, float(li["tape"].encode("utf-8")) / 10000)  # bet365初盘 让球
                    sheet.write(row, 37, float(li["awayOdds"].encode("utf-8")) / 10000)  # bet365初盘 客队赔率
            row=row+1
        return  row
    # 确定好excel的标题，即第一行
    def excel_head(self,sheet):
        # excel表格表头
        sheet.write(0, 0, "比赛id")  # 名称
        sheet.write(0, 1, "时间")  # 名称
        sheet.write(0, 2, "星期")  # 基金代码
        sheet.write(0, 3, "比赛类型")  # 风险等级
        sheet.write(0, 4, "月份")  # 净值
        sheet.write(0, 5, "时间点")  # 投资风格
        sheet.write(0, 6, "主队排名")  # 基金经理
        sheet.write(0, 7, "主队")  # 截至日期
        sheet.write(0, 8, "比分")  # ？2.99
        sheet.write(0, 9, "客队")  # 4.55
        sheet.write(0, 10, "客队排名")  # 近一周阶段涨幅%
        sheet.write(0, 11, "半场比分")  # 近一月
        sheet.write(0, 12, "竞彩赔率")  # 近三月
        sheet.write(0, 13, "让球赔率")  # 近半年
        sheet.write(0, 14, "澳门初盘主队赔率")  # 近一年
        sheet.write(0, 15, "澳门初盘让球")  # 近一年
        sheet.write(0, 16, "澳门初盘客队赔率")  # 近一年
        sheet.write(0, 17, "澳门终盘主队赔率")  # ？
        sheet.write(0, 18, "澳门终盘让球")  # ？
        sheet.write(0, 19, "澳门终盘客队赔率")  # ？

        sheet.write(0, 20, "bet365初盘主队赔率")  # 近一年
        sheet.write(0, 21, "bet365初盘让球")  # 近一年
        sheet.write(0, 22, "bet365初盘客队赔率")  # 近一年
        sheet.write(0, 23, "bet365终盘主队赔率")  # ？
        sheet.write(0, 24, "bet365终盘让球")  # ？
        sheet.write(0, 25, "bet365终盘客队赔率")  # ？

        sheet.write(0, 26, "澳门初盘大球赔率")  # 近一年
        sheet.write(0, 27, "澳门初盘总进球数")  # 近一年
        sheet.write(0, 28, "澳门初盘小球赔率")  # 近一年
        sheet.write(0, 29, "澳门终盘大球赔率")  # ？
        sheet.write(0, 30, "澳门终盘总进球")  # ？
        sheet.write(0, 31, "澳门终盘小球赔率")  # ？

        sheet.write(0, 32, "bet365初盘大球赔")  # 近一年
        sheet.write(0, 33, "bet365初盘总进球数")  # 近一年
        sheet.write(0, 34, "bet365初盘小球赔率")  # 近一年
        sheet.write(0, 35, "bet365终盘大球赔率")  # ？
        sheet.write(0, 36, "bet365终盘总进球")  # ？
        sheet.write(0, 37, "bet365终盘小球赔率")  # ？




    def readExl2Dic(self,name):
        """获取当前路径"""
        curpath = os.path.dirname(__file__)
        """获取excel文件【与当前脚本在同一级目录下】"""
        filename = os.path.join(curpath, name)

        excel_handle = xlrd.open_workbook(filename)  # 路径不包含中文
        # sheet1 = self.excel_handle.sheet_names()[1]           # 获取第1个sheet的名字,可与获取name函数一起使用
        # sheet = self.excel_handle.sheet_by_name('Sheet1')     # 根据名字获取
        sheet = excel_handle.sheet_by_index(0)  # 根据索引获取第一个sheet
        # print sheet.name,sheet.nrows,sheet.ncols         # 获取sheet的表格名称、总行数、总列数
        row_num = sheet.nrows  # 行
        #  col_num = sheet.ncols       # 列
        dic = {}
        row1 = sheet.row_values(0)
        # 因为是Unicode编码格式，因此需要转成utf-8
        for i in range(1, row_num):
            # dic[row1[0].encode('utf-8')] = self.sheet.row_values(i)[0].encode('utf-8')
            dic[sheet.row_values(i)[0]] = sheet.row_values(i)[5]
        return dic

    def Dic2Exl(self,dic):
        # 创建excel
        wbk = xlwt.Workbook("utf-8")
        sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        # for fund in dic.keys:
        #     if dic[fund].contain(','):
                # sheet.write(fund, 0, fund_dic["name"])  # 名称

    def FormatExl(self):
        excel_handle = xlrd.open_workbook('20.xls')  # 路径不包含中文
        sheet = excel_handle.sheet_by_index(0)  # 根据索引获取第一个sheet
        # print sheet.name,sheet.nrows,sheet.ncols         # 获取sheet的表格名称、总行数、总列数
        row_num = sheet.nrows  # 行
        exl_list=[]
        # 因为是Unicode编码格式，因此需要转成utf-8
        for i in range(0, row_num):
            try:
                l=[]
                json_data=sheet.row_values(i)[2]
                answer_type=sheet.row_values(i)[3]
                intent=''
                point=''
                test={}
                if(answer_type.find('语义引擎')>=0):
                    if(json_data.find('唱歌')>-1):
                        intent='唱歌'
                    elif (json_data.find('讲故事')>-1):
                        intent = '讲故事'
                    else:
                        test = json.loads(json_data)
                    ss=json_data.find('失败')
                    if (json_data.find(u'失败') >-1) :
                        continue

                    # test = json.loads(json_data)
                    if(json_data.find('point')>-1):
                        point=test[u'point']
                    if(json_data.find('place')>-1  and json_data.find('讲故事')==-1):
                        point=test[u'place']
                    if len(intent)==0:
                        intent=test[u'intent']

                l.append(sheet.row_values(i)[0])
                if answer_type.find('小艾')>-1:
                    l.append(sheet.row_values(i)[2])
                else:
                    l.append(sheet.row_values(i)[1])
                l.append(intent)
                l.append(point)
                l.append(sheet.row_values(i)[3])
                l.append(sheet.row_values(i)[4])
            except:
                print(json_data)
                print('dddd')
            exl_list.append(l)
        # 创建excel
        wbk = xlwt.Workbook("utf-8")
        sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        row = 0

        for rows_data in exl_list:
            try:
                if(len(rows_data)==6 and len(rows_data[2])>0 or rows_data[4].find('小艾')>-1):
                    sheet.write(row, 0, rows_data[0])
                    sheet.write(row, 1, rows_data[1])
                    sheet.write(row, 2, rows_data[2])
                    sheet.write(row, 3, rows_data[3])
                    sheet.write(row, 4, rows_data[4])
                    sheet.write(row, 5, rows_data[5])
                    row = row + 1
            except:
                print 'ddddddd'
        wbk.save('8686.xls')
    def FormatExl_all(self):
        excel_handle = xlrd.open_workbook('log_nongshang.xls')  # 路径不包含中文
        sheet = excel_handle.sheet_by_index(0)  # 根据索引获取第一个sheet
        # print sheet.name,sheet.nrows,sheet.ncols         # 获取sheet的表格名称、总行数、总列数
        row_num = sheet.nrows  # 行
        exl_list=[]
        # 因为是Unicode编码格式，因此需要转成utf-8
        for i in range(0, row_num):
            try:
                l=[]
                l.append(sheet.row_values(i)[0])
                l.append(sheet.row_values(i)[1])
                l.append(sheet.row_values(i)[2])
                l.append(sheet.row_values(i)[3])
                l.append(sheet.row_values(i)[4])
                l.append(sheet.row_values(i)[5])
            except:
                print('dddd')
            exl_list.append(l)
        # 创建excel
        wbk = xlwt.Workbook("utf-8")
        sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
        row = 0

        for rows_data in exl_list:
            try:
                sheet.write(row, 0, rows_data[0])
                sheet.write(row, 1, rows_data[1])
                if(rows_data[2].find('{')>-1):
                    test = json.loads(rows_data[2])
                    if(rows_data[2].find('intent')>-1):
                        sheet.write(row, 2, test['intent'])
                    else:
                        sheet.write(row, 2, '')
                else:
                    sheet.write(row, 2, rows_data[2])
                sheet.write(row, 3, rows_data[3])
                sheet.write(row, 4, rows_data[4])
                sheet.write(row, 5, rows_data[5])
                row = row + 1
            except:
                print 'ddddddd'
        wbk.save('8686.xls')

    def get_week_day(self,str):#str='190422'

        d=datetime.date(int(str[0:2])+2000,int(str[2:4]),int(str[4:6]))
        w=datetime.date.weekday(d)
        return self.week_day_dict[w]
# #
if __name__ == '__main__':
    # # 创建类
    url = "https://live.aicai.com"#https://live.aicai.com/static/no_cache/jc/zcnew/data/hist/190405zcRefer.js
    test = Crawler_Fund_table(url)

    wbk = xlwt.Workbook("utf-8")
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    test.excel_head(sheet)  # excel的标题

    # # 第一步 将数据读取到磁盘 txt
    # #遍历日期 20130130-20190514
    # start = '2013-03-11'
    # end = '2019-05-14'
    # datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    # dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    # while datestart < dateend:
    #     try:
    #         datestart += datetime.timedelta(days=1)
    #         # print datestart.strftime('%Y-%m-%d')#2019-05-14
    #         # print datestart.strftime('%Y%m%d')[-6:]#190514
    #         # 1、
    #         data_url = 'https://live.aicai.com/static/no_cache/jc/zcnew/data/hist/' + datestart.strftime('%Y%m%d')[
    #                                                                                   -6:] + 'zcRefer.js'
    #         test.date = data_url[-16:-10]
    #         test.GetHtml(data_url)
    #         test.StrToTxt(name='matchdata' + test.date + '.txt')  # 将爬取的html写到txt
    #         # 2、
    #         matchlist = test.GetHtml(
    #             'https://live.aicai.com/jsbf/timelyscore!dynamicMatchDataForJczq.htm?dateTime=' + datestart.strftime(
    #                 '%Y-%m-%d'))
    #         test.StrToTxt(name='matchlist' + test.date + ".txt")  # 将爬取的html写到txt
    #         # 3、去除网页中的空行和空格
    #         p = re.compile('\s+')
    #         new = re.sub(p, '', matchlist)
    #         # rex为正则表达式nmatchArr[0] = '1584880^237^2019-04-05 16:50^18:00^-1^#FF7000^周五001^澳洲甲^墨尔本城^布里斯班'.split('^');
    #         rex = 'nmatchArr\[.*?\]=\'(.*?)\'\.split'
    #         pattern = re.compile(rex)
    #         # items = re.findall(pattern, new, 0, 50)
    #         items = pattern.findall(new)  # list
    #         for item in items:
    #             list = item.split("^")
    #             test.matchid = list[0]
    #             # 4、
    #             rangqiu = test.GetHtml(
    #                 'https://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=' + list[
    #                     0] + '&propId=0&start=0&size=50&selectedType=yazhi')
    #             test.StrToTxt(name='rangqiu' + test.date + list[0] + ".txt")  # 将爬取的html写到txt
    #             # 5、
    #             jinqiu = test.GetHtml(
    #                 'https://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=' + list[
    #                     0] + '&propId=0&start=0&size=50&selectedType=dxzhi')
    #             test.StrToTxt(name='jinqiu' + test.date + list[0] + ".txt")  # 将爬取的html写到txt
    #             time.sleep(1)
    #     except Exception, e:
    #         f = open('log-http.txt', 'a+')
    #         f.writelines(datestart.strftime('%Y%m%d')[-6:] + "   " + test.matchid + "\r\n")
    #         f.close()








    # 第二步 将txt数据写到excel中  遍历日期 20130130-20190514
    # start = '2013-01-30'
    # end = '2019-05-14'
    # row = 1
    # f = open('log-toexl.txt', 'w+')
    # datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    # dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    # while datestart < dateend:
    #     try:
    #         datestart += datetime.timedelta(days=1)
    #         # print datestart.strftime('%Y-%m-%d')#2019-05-14
    #         # print datestart.strftime('%Y%m%d')[-6:]#190514
    #         if datestart.strftime('%Y%m%d')[-6:] =='130212':
    #             print "hhh"
    #         # 1、
    #         matchdata = test.TxtToStr('data\\matchdata' + datestart.strftime('%Y%m%d')[-6:] + '.txt')  # 将磁盘的txt读取到str
    #         strs = matchdata.replace("'", '"')
    #         matchdata_json = json.loads(strs)  # dic
    #
    #         matchlist = test.TxtToStr('data\\matchlist' + datestart.strftime('%Y%m%d')[-6:] + ".txt")  # 将磁盘的txt读取到str
    #         # 去除网页中的空行和空格
    #         p = re.compile('\s+')
    #         new = re.sub(p, '', matchlist)
    #         # rex为正则表达式nmatchArr[0] = '1584880^237^2019-04-05 16:50^18:00^-1^#FF7000^周五001^澳洲甲^墨尔本城^布里斯班'.split('^');
    #         rex = 'nmatchArr\[.*?\]=\'(.*?)\'\.split'
    #         pattern = re.compile(rex)
    #         # items = re.findall(pattern, new, 0, 50)
    #         items = pattern.findall(new)  # list
    #         # 写excels
    #         row=test.write_excel_mainpage(matchdata_json, items, row, sheet, datestart.strftime('%Y%m%d')[-6:])
    #     except  Exception, e:
    #         f.writelines(datestart.strftime('%Y%m%d')[-6:] + "   " + test.matchid)
    #
    # f.close()
    #
    #
    # wbk.save('football.xls')

    # 有些数据没读全，重新读取数据
    # 遍历日期 20130130-20190514
    start = '2014-08-21'
    end = '2019-05-14'
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        try:
            datestart += datetime.timedelta(days=1)

            # 2、
            matchlist = test.TxtToStr('data\\matchlist' + datestart.strftime('%Y%m%d')[-6:] + ".txt")
            # 3、去除网页中的空行和空格
            p = re.compile('\s+')
            new = re.sub(p, '', matchlist)
            # rex为正则表达式nmatchArr[0] = '1584880^237^2019-04-05 16:50^18:00^-1^#FF7000^周五001^澳洲甲^墨尔本城^布里斯班'.split('^');
            rex = 'nmatchArr\[.*?\]=\'(.*?)\'\.split'
            pattern = re.compile(rex)
            # items = re.findall(pattern, new, 0, 50)
            items = pattern.findall(new)  # list
            for item in items:
                list = item.split("^")
                test.matchid = list[0]
                # 4、
                rangqiu = test.GetHtml(
                    'https://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=' + list[
                        0] + '&propId=0&start=0&size=50&selectedType=yazhi')
                test.StrToTxt(name='rangqiu' + datestart.strftime('%Y%m%d')[-6:] + list[0] + ".txt")  # 将爬取的html写到txt
                # 5、
                jinqiu = test.GetHtml(
                    'https://live.aicai.com/xiyaou/odds!getyazhi.htm?betId=' + list[
                        0] + '&propId=0&start=0&size=50&selectedType=dxzhi')
                test.StrToTxt(name='jinqiu' + datestart.strftime('%Y%m%d')[-6:] + list[0] + ".txt")  # 将爬取的html写到txt
                print datestart.strftime('%Y%m%d')[-6:] + list[0]
            # time.sleep(1)  # 时间必须长一些，不然数据来不及存入到txt中
        except Exception, e:
            f = open('log-http.txt', 'a+')
            f.writelines(datestart.strftime('%Y%m%d')[-6:] + "   " + test.matchid + "\r\n")
            f.close()

    print ('The End')