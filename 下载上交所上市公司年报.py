from pathlib import Path
from shreport import SH

#设置本地计算机上交所网站的cookie信息
#cookies = {"Cookie": '您的cookies'}
cookies = {'Cookie': 'yfx_c_g_u_id_10000042=_ck21092411170413074181346583754; VISITED_MENU=%5B%228911%22%2C%228528%22%2C%229062%22%2C%228352%22%5D; VISITED_COMPANY_CODE=%5B%22600026%22%2C%22600000%22%2C%22600246%22%5D; VISITED_STOCK_CODE=%5B%22600026%22%2C%22600000%22%2C%22600246%22%5D; seecookie=%5B600026%5D%3A%u4E2D%u8FDC%u6D77%u80FD%2C%5B600000%5D%3A%u6D66%u53D1%u94F6%u884C%2C%5B600246%5D%3A%u4E07%u901A%u53D1%u5C55; yfx_f_l_v_t_10000042=f_t_1632453424300__r_t_1632745414488__v_t_1632745414488__r_c_3;'}
#cookies = {'Cookie': 'yfx_c_g_u_id_10000042=_ck20040811130118223273975003072; VISITED_MENU=%5B%228312%22%2C%228352%22%5D; VISITED_COMPANY_CODE=%5B%22600277%22%2C%22603383%22%2C%22601857%22%5D; VISITED_STOCK_CODE=%5B%22600277%22%2C%22603383%22%2C%22601857%22%5D; seecookie=%5B600277%5D%3A%u4EBF%u5229%u6D01%u80FD%2C%5B603383%5D%3A%u9876%u70B9%u8F6F%u4EF6%2C%5B601857%5D%3A%u4E2D%u56FD%u77F3%u6CB9; yfx_f_l_v_t_10000042=f_t_1586315581606__r_t_1587454757049__v_t_1587454757049__r_c_1; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042='}

sh = SH(cookies)
#获取当前代码所在的文件夹路径
cwd = Path().cwd()
cwd=Path('c:\\test')

#以浦发银行为例股票代码600000
sh.download(code='600066', savepath=cwd)