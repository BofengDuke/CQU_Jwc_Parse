#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
Description: 连接 Mongodb 数据库
'''

from pymongo import MongoClient
from config import HOST,PORT

class Mongodb():
	def __init__(self,client=None):
		self.client = MongoClient(HOST,PORT) if client is None else client
		self.db = self.client.cqudata

	def setSchedule(self,stu_num,schedule):
		""" 存储学生课表
		@param:
			stu_num: 学生学号
			schedule: 学生课表
		"""
		record = {
			'schedule':schedule
		}
		self.db.schedule.update({'_id':stu_num},{'$set':record},upsert=True)

	def getSchedule(self,stu_num):
		""" 查询并获取学生课表
		@param:
			stu_num: 学生学号
		"""
		record = self.db.schedule.find_one({'_id':stu_num})
		if record:
			return record['schedule']
		else:
			raise KeyError(str(stu_num)+' does not have schedule record.')

	def clear(self):
		self.db.schedule.drop()
		print('success')