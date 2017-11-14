#-*- coding:utf-8 -*-

# url: jxgl.cqu.edu.cn 
# config the login username and password

# STU_NUM : 学号
# PASSWORD: 登录教务处的密码

STU_NUM = 	
PASSWORD = ''

# 默认头部信息
HEADERS = {
	'Host':'jxgl.cqu.edu.cn',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-US,en;q=0.5',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}

# 登录的URL，需要先访问该链接，获取登录数据
LOGIN_URL = 'http://jxgl.cqu.edu.cn/_data/index_login.aspx'

# 登录后的主网页链接，（好像所有想获得的数据，都是通过发送参数给它）
MAIN_URL = 'http://jxgl.cqu.edu.cn/MAINFRM.aspx'

# 获取课表的URL,同时还需要重定向指向该链接
SCHEDULE_URL = 'http://jxgl.cqu.edu.cn/znpk/Pri_StuSel_rpt.aspx'



# ----------------------------------------------------------
# ----------------------------------------------------------
# Database base config
HOST = 'localhost'
PORT = 27017
