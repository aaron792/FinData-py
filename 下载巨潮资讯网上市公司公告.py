from pathlib import Path
from cninfo import CNINFO

cf = CNINFO()
#指定下载页面、证券代码、是否返回查到结果的总数、起止日期，获得各个公告的下载url
pl=cf.get_pdf_list(1, "000011", "2020-03-17", "2022-09-22")
print(pl)
save_path = Path('D:\\testCN')
cf.download_pdflist(pl,save_path)

print(cf.get_orgId("600057"))

