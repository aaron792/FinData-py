import szreport
from szreport import *;

sz=szreport.SZ()

# first post
file_url = "http://disc.static.szse.cn/download"
res = sz.get_resp_jNode(1, 30)
for i in res['data']:
    sz.pdf_list.append(file_url+i['attachPath'])
    sz.name_list.append(sz.format_title(i['title']))

# 计算页数
total = res['announceCount']
#page_nums = total / 30 + 1
page_nums = 500
page_index = 500

print('正在检索...')
while page_index <= page_nums:
    res = sz.get_resp_jNode(page_index, 30)
    # print(res['data'])
    for i in res['data']:
        print(i['secCode'][0]+"--"+i['secName'][0]+"--"+i['title']+"--"+i['publishTime'])
        sz.pdf_list.append(file_url+i['attachPath'])
        sz.name_list.append(sz.format_title(i['title']))
    page_index += 1

print('已查找到所有下载链接，共:', len(sz.pdf_list), '条')

# 下载
save_dir = 'D:\\szTest\\'
sz.download_and_extract(sz.pdf_list, sz.name_list,save_dir)

print(sz.announcement_count())
print(sz.get_stock_name("002569"))
