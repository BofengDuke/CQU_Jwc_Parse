#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
Author:	Duke
Description: 分析并获取教务处信息
'''

import lxml.html
import requests
import hashlib
from config import STU_NUM,PASSWORD,LOGIN_URL,HEADERS,SCHEDULE_URL
from mongodb import Mongodb

class Parsejwc(object):
	"""Parse CQU jwc data,and save data"""
	def __init__(self, stu_num,passwd):
		"""
		@param:
			stu_num:   学生学号
			passwd:  登录密码
		"""
		self.stu_num = stu_num
		self.passwd = passwd
		self.session = None
		

	def parse_login_form(self):
		""" 解析登录页面，并获取表单的参数,并返回登录表单数据
		"""
		html = requests.get(LOGIN_URL).text 

		# 获取表单中input的参数
		"""
		表单参数描述：
			txt_dsdsdsdjkjkjc ： 学号/用户名/STU_NUM
			txt_dsdfdfgfouyy  :  原密码，但传给服务器的是空值
			efdfdfuuyyuuckjg  ： 加密的密码，传给服务器
		"""
		tree = lxml.html.fromstring(html)
		data = {}
		for e in tree.cssselect("form input"):
			if e.get('name'):
				data[e.get('name')] = e.get('value')

		# 获取 select 的参数，选择身份，默认是学生
		data['Sel_Type'] = 'STU'
		data['txt_dsdsdsdjkjkjc'] = int(self.stu_num)
		data['efdfdfuuyyuuckjg'] = self.__encrypt_passwd(self.stu_num,self.passwd)

		return data

	def login(self,headers=HEADERS):
		"""	登录到主页中，获取登录会话，以方便进一步操作
		@param:
			headers: 请求的头部信息，默认加载 config 文件中的 HEADERS
			stu_num: 学生学号
			passwd:  登录密码
		"""
		headers = headers 
		form_data = self.parse_login_form()
		s = requests.Session()
		s.headers.update(headers)
		s.post(LOGIN_URL,data=form_data)
		self.session = s

	def download_schedule(self,param=None,db_client=None):
		""" 获取课表,这里默认获取个人课表
		@param:
			param:{				# 给服务器传递的 param 参数
				Sel_XNXQ: 		# 20161 表示查看个人课表
				rad: on
				px: 1       	# 0: 按课程/环节查询课表，1：按时间查询课表
				zc_flag: 1  	# 表示按周数排序，默认不传
				zc_input: 1-18  # 表示1-18周，默认不传
			}
		"""
		if self.session is None:
			self.login()
		POST_DATA = {
			'Sel_XNXQ':20161,
			'rad':'on',
			'px': 1  	
		}
		post_data = param if param else POST_DATA
		
		r = self.session.post(SCHEDULE_URL,data=post_data,headers={'Referer':SCHEDULE_URL})
		tree = lxml.html.fromstring(r.text)
		page_table = tree.cssselect('.page_table')
		tr_list = tree.cssselect('.page_table tbody > tr')

		# Parse the course data 
		schedules = []
		for tr in tr_list:
			td_list = tr.cssselect('td')[1:]
			course = []
			for td in td_list:
				course.append(lxml.html.tostring(td,method='text',encoding='utf-8'))
			schedules.append(course)

		# Decode the data that have been encoded by lxml.html.tostring
		for i in range(len(schedules)):
			for j in range(len(schedules[i])):
				schedules[i][j] = schedules[i][j].decode('utf-8')

		
		self.__save_schedule(stu_num=self.stu_num,schedules=schedules,db_client=db_client)


	def __save_schedule(self,stu_num,schedules,db_client=None):
		""" 保存得到的课表
		@param:
			stu_num: 学生学号
			schedules: 学生课表,list 类型
		"""
		db = Mongodb() if db_client is None else db_client
		db.setSchedule(int(stu_num),schedules)

	def get_schedule(self,stu_num,db_client=None):
		""" 获取学生课表
		@param:
			stu_num: 学生学号
		"""
		db = Mongodb() if db_client is None else db_client
		try:
			return db.getSchedule(int(stu_num))
		except KeyError as e:
			print ('[Error] get_schedule() is error: {}'.format(e))


	def __encrypt_passwd(self,stu_num,password):
		""" 网站中，传送给服务器的密码是经过加密的，并赋值给其他表单
		原加密算法(javascript)如下，，
		s=md5(stu_num+md5(password.value).substring(0,30).toUpperCase()+schoolcode).substring(0,30).toUpperCase();
		@param:
			stu_num:  原账号
			password: 原密码 

		schoolcode : 10611
		"""
		schoolcode=10611
		stu_num = str(stu_num)
		password = str(password).encode()
		schoolcode = str(schoolcode)
		md = hashlib.md5()
		md.update(password)
		prev = stu_num + md.hexdigest()[0:30].upper() + schoolcode
		prev = prev.encode()
		md2 = hashlib.md5()
		md2.update(prev)
		pwd = md2.hexdigest()[0:30].upper()
		return pwd


if __name__ == '__main__':
		
	jwc = Parsejwc(STU_NUM,PASSWORD)

	print(get_schedule(STU_NUM))