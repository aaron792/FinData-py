import urllib.request
import urllib.parse
import time
import requests
import grequests
import datetime
import csv
import urllib.request
import urllib.parse
import json
import sys
import os
import re

class SZ(object):
    url = "http://www.szse.cn/api/disc/announcement/annList?random=0.9794648678933643"

    #http请求中的头文件
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'HOST': 'www.szse.cn',
        'Origin': 'http://www.szse.cn',
        'Referer': 'http://www.szse.cn/disclosure/listed/notice/index.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'X-Request-Type': 'ajax',
        'X-Requested-With': 'XMLHttpRequest'
    }

    bigCategoryId = ["010301"]
    bigIndustryCode = ["C"]
    channelCode = ["listedNotice_disc"]
    plateCode = ["11"]
    seDate = ["", ""]

    #记录要爬取的url和上市公司财报的名称
    pdf_list = []  # 保存pdf链接地址
    name_list = []  # 保存pdf文件名

    def __init__(self):
        print("实例被创建")

    #获取深交所允许下载的公告总数
    def announcement_count(self):
        resp_jnode = self.get_resp_jNode(1,30)
        return resp_jnode['announceCount']

    #深交所每个页面显示30份可下载的公告，获取下载公告的总页数
    def announcement_page_count(self): #返回深交所查询公告网页的总页数
        return self.announcement_count()/30

    def get_stock_name(self,stock_code):
        """根据输入的证券代码，返回股票名称
              Parameter:
                  stock_code: str 证券代码
              Return:
                  str变量: str 若从上市公司列表中找到该代码，返回上市公司名称，否则返回“-1”
        """
        page_nums=self.announcement_page_count()
        page_index=1
        while page_index <= page_nums:
            #print(page_index)
            res = self.get_resp_jNode(page_index, 30)
            if 'data' in res:
                # print(res['data'])
                for i in res['data']:
                    if (stock_code == i['secCode'][0]):
                        return i['secName'][0]
            page_index+=1
        return "-1"

    def get_resp_jNode(self,pageNum, pageSize):
        """获取第pageNum页的json文件，文件中记录30份披露报告的所有目录信息
              Parameter:
                  pageNum: str  页码，起始页码
                  pageSize: int 页数（固定：30），深交所网站将每个网页json文件的上市公司数量固定为30个
              Return:
                  res: list 获取的表格内容
        """
        params = {
            'seDate': self.seDate,
            'bigCategoryId': self.bigCategoryId,
            'bigIndustryCode': self.bigIndustryCode,
            'channelCode': self.channelCode,
            'pageNum': pageNum,
            'pageSize': pageSize,
            'plateCode': self.plateCode
        }
        request = urllib.request.Request(url=self.url, headers=self.headers)
        #print(request.full_url)
        #把python对象转换成json对象，encode()将编码转换为可读的中文
        formdata = json.dumps(params).encode()  # urllib.parse.urlencode(params).encode()
        #print(formdata)
        response = urllib.request.urlopen(request, formdata)
        res_json = response.read().decode()
        #print(res_json)
        res = json.loads(res_json)
        return res

    def format_title(self,title):
        """去除公告文件名中的特殊符号，以备存储，公告名中包含的某些特殊符号无法作为windows文件的文件名
           Parameter:
               title: str  需要处理的文件名称
           Return:
               new_title: str 没有特殊符号的文件名
        """
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title) + '.pdf'  # 替换为下划线
        return new_title

    def download_rep(self,rep_url_list,rep_name_list, save_dir):
        """根据给定的URL地址下载文件
        Parameter:
            rep_url_list: list 文件的URL路径地址列表
            rep_name_list: list 公告文件名称的列表
            save_dir: str  保存路径
        Return:
            None
        """
        #for rep_url, rep_name,index in zip(rep_url_list, rep_name_list,range(len(rep_url_list))):
        for rep_url, rep_name in zip(rep_url_list, rep_name_list):
            print('\n开始下载'+rep_name)
            print('\n为防范网站的反爬措施，等待30s')
            time.sleep(30)#为防范网站的反爬措施，等待30s
            # filename = url.split('/')[-1]
            #filename = self.name_list[index]
            save_path = os.path.join(save_dir, rep_name)
            urllib.request.urlretrieve(rep_url, save_path)
            #sys.stdout.write('\r>> Downloading %.1f%%' % (float(index + 1) / float(len(rep_url_list)) * 100.0))
            #sys.stdout.flush()
        print('\n下载完毕')

    def download_rep_by_stock_code(self, stock_code, save_dir):
        """根据输入的证券代码，下载该上市公司的所有公告文件
        Parameter:
            stock_code: str 上市公司的证券代码
            save_dir: str  公告文件的保存路径
        Return:
            None
        """
        rep_url_list=[] #存储该企业的财报下载url
        rep_name_list=[] #存储财报名称

        page_nums = self.announcement_page_count()#计算待爬取的页面总数
        page_index = 1
        download_url_prefix = "http://disc.static.szse.cn/download"#公告下载地址的前缀
        #获取待爬取的公告url和公告名称
        while page_index <= page_nums:
            time.sleep(3)#为防范网站的反爬措施，等待3s
            res = self.get_resp_jNode(page_index, 30)
            if 'data' in res:
                # print(res['data'])
                for i in res['data']:
                    if (stock_code == i['secCode'][0]):
                        print(i['secCode'][0] + "--" + i['secName'][0] + "--" + i['title'] + "--" + i['publishTime'])
                        rep_url_list.append(download_url_prefix + i['attachPath'])
                        rep_name_list.append(self.format_title(i['title']))
                page_index += 1
        #下载公告
        self.download_rep(rep_url_list,rep_name_list,save_dir)