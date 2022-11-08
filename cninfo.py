# 前面的一些参数PLATE CATEGORY等是向服务器请求时要发送过去的参数。
# !/usr/bin/python
# coding = utf-8
# __author__='aaron792'
# description:下载csv中列出的pdf年报

import csv
import os
import time
from pathlib import Path
import requests

class CNINFO(object):
    OUTPUT_FILENAME = 'report'
    # 板块类型：沪市：shmb；深市：szse；深主板：szmb；中小板：szzx；创业板：szcy；
    PLATE = 'szzx;'
    # 公告类型：category_scgkfx_szsh（首次公开发行及上市）、category_ndbg_szsh（年度报告）、category_bndbg_szsh（半年度报告）
    #CATEGORY = '' #包含所有公告
    CATEGORY = 'category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh'
    URL = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'#查询url
    # 使用浏览器代理，否则网站检测到是Python爬虫时会自动屏蔽
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    MAX_PAGESIZE = 30 #查询页面默认返回30条查询信息
    MAX_RELOAD_TIMES = 5
    RESPONSE_TIMEOUT = 10

    #获取巨潮资讯网内给每个上市公司定义的orgid，该id在爬取该公司年报中会用到
    def get_orgId(self,stock_code):
        url="http://www.cninfo.com.cn/new/data/szse_stock.json"
        resp = requests.post(url, self.HEADER, timeout=self.RESPONSE_TIMEOUT).json()
        #print(resp)
        for i in resp['stockList']:
            #print(i['code'])
            if (stock_code == i['code']):
                return i['orgId']
        return "-1"

    # 参数：页面id(每页条目个数由MAX_PAGESIZE控制)，是否返回总条目数(bool)
    #按照上市公司的证券代码，起止日期，与显示页面编号查询该上市公司公告的下载url
    def get_pdf_list(self,page_num, stock_code, start_date='2019-01-01', end_date='2022-09-01'):
        """按照上市公司的证券代码，起止日期，与显示页面编号查询该上市公司公告的下载url
              Parameter:
                  page_num: str 查询结果页面的页码
                  stock_code: str 证券代码
                  start_date: str 起始日期
                  end_date: str 终止日期
              Return:
                  pdf_list: 二维元素列表 列表中的每个元素是一个二元列表，二元列表的第一个元素存储公告的名称，第二个元素存储公告下载的url
        """
        #生成下方query参数中的stock_info和colum_info参数
        stock_info = str(stock_code) + ","+self.get_orgId(stock_code)
        column_info = 'szse'
        if stock_code.startswith("60"):
            #stock_info = str(stock_code) + ",gssh0" + str(stock_code)
            column_info = 'sse'
        #if stock_code.startswith("30"):
            #stock_info = str(stock_code) + ",9900015690"

        # 这是查询参数
        query = {
            'stock': stock_info,
            'searchkey': '',
            'plate': '',
            'category': self.CATEGORY,
            'trade': '',
            'column': column_info,  # 注意沪市为sse
            'pageNum': page_num,
            'pageSize': self.MAX_PAGESIZE,
            'tabName': 'fulltext',
            'sortName': '',
            'sortType': '',
            'limit': '',
            'showTitle': '',
            'seDate': start_date + '~' + end_date,
            'isHLtitle': 'true'
        }
        pdf_list = []
        resp = requests.post(self.URL, query, self.HEADER, timeout=self.RESPONSE_TIMEOUT).json()#向网站服务器查询
        print(resp)
        print("总共查询到的链接数为：" + str(resp['totalRecordNum']))
        if resp['announcements'] is not None:
            for ann in resp['announcements']:
                pdf_url = 'http://static.cninfo.com.cn/' + str(ann['adjunctUrl'])
                print(pdf_url)
                print(str(ann['secCode']) + str(ann['secName']) + str(ann['announcementTitle']) + pdf_url[-pdf_url[::-1].find('.') - 1:])  # 最后一项是获取文件类型后缀名)
                pdf_name = str(ann['secCode']) + str(ann['secName']) + str(ann['announcementTitle']) + pdf_url[-pdf_url[::-1].find('.') - 1:]  # 最后一项是获取文件类型后缀名
                pdf_list.append([pdf_name, pdf_url])
        return pdf_list

    def download_rpt(self,rpt_url,rpt_name,save_path):
        """下载单个公告文件，rpt_url是公告下载链接，rpt_name是公告名称，save_path是保存路径，即保存公告文件的文件夹
              Parameter:
                  rpt_url: str  公告下载链接
                  rpt_name: str 公告名称
              Return:
                  save_path: str 保存路径，即保存该公告文件的文件夹，公告文件以公告名称命名
        """
        time.sleep(3) #每次下载停顿3s，防网站反爬虫
        rep=requests.get(rpt_url)#下载公告
        path=Path(save_path).joinpath(*('disclosure', 'reports'))
        path.mkdir(parents=True, exist_ok=True)
        rpt_path = path.joinpath(rpt_name.replace(" ",""))#生成公告文件
        with open(rpt_path, 'wb') as rpt:
            rpt.write(rep.content)
            print('已成功下载{}'.format(rpt_name))

    #下载多个公告文件，pdf_list是2维元素的列表，列表中每个元素的第一个元素是待下载pdf文件的文件名，第二个元素是pdf文件uri
    def download_pdflist(self,pdf_list,save_path): #pdf_list里存储一系列的数组，每个数组包含两个元素，第一个元素是下载文件名，第二个元素是下载文件名的url
        for pdf_info in pdf_list:
            self.download_rpt(pdf_info[1],pdf_info[0],save_path)

#测试
cf = CNINFO()
#指定下载页面、证券代码、是否返回查到结果的总数、起止日期，获得各个公告的下载url
pl=cf.get_pdf_list(1, "000011", "2020-03-17", "2022-09-22")
print(pl)