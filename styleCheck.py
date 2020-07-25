#!/usr/bin/python
#-*- coding: utf-8  -*-

import os
import re
import json

'''
This program can only be used in the same 
directory as the detect reports
'''

JSON_FILE = "preDefineRule.json"

class styleCheck:
	def __init__(self):
		pass

	def getFileNumAndName(self):
		fileList = os.listdir()	
		solList = list()
		reportList = list()
		for f in fileList:
			if ".sol" in f and "_format" not in f and "No" not in f:
				solList.append(f)
			elif "_detect.report" in f:
				reportList.append(f)
		print("Contract number: ", len(solList))
		print("Report number: ", len(reportList))
		print("Generated percent: ", len(reportList) / len(solList))
		return reportList

	def filterBlankEle(self, _list):
		eleList = list()
		for item in _list:
			if item == "":
				continue
			else:
				eleList.append(item)
		return eleList

	def getContent(self, _path):
		with open(_path, "r", encoding = "utf-8") as f:
			return f.read()
		return str()

	def splitContentAccordBlankLine(self, _str):
		lineList = _str.splitlines(True)
		#print(lineList)
		resultList = list()
		temp = str()
		for line in lineList:
			if line != "\n":
				temp += line
			else:
				resultList.append(temp)
				temp = str()
				continue
		resultList = self.filterBlankEle(resultList)
		return resultList

	def getPredefineRule(self):
		jsonStr = str()
		with open(JSON_FILE, "r", encoding = "utf-8") as f:
			jsonStr = f.read()
		jsonDict = json.loads(jsonStr)
		return jsonDict


	def checkFormat(self, _contentList):
		'''
		语料库返回格式: <label -> [fotmat 1, format 2]>
		'''
		flag = True
		#1. 读取预定义规则
		ruleDict = self.getPredefineRule()
		#print(ruleDict)
		#2. 按元素进行匹配
		for index in range(len(_contentList)):
			_index = str(index + 1)
			if self.checkEachRule(_contentList[index], ruleDict[_index]):
				continue
			else:
				flag = False
				break
		return flag

	def checkEachRule(self, _str, _ruleList):
		pattern1 = _ruleList[0]
		pattern2 = _ruleList[1]
		if re.match(pattern1, _str, re.S) != None or re.match(pattern2, _str, re.S) !=None:
			return True
		else:
			return False




	def doCheck(self):
		#1. 获取检测报告的路径
		reportList = self.getFileNumAndName()
		rightNum = 0
		wrongNum = 0
		#2. 检查每一份报告的格式
		for report in reportList:
			content = self.getContent(report)
			#2.1 按空行进行切分
			contentList = self.splitContentAccordBlankLine(content)
			#2.2 根据语料库，检查格式
			if self.checkFormat(contentList):
				rightNum += 1
			else:
				wrongNum += 1
		print("Correctly formatted number: ", rightNum)
		print("Wrong formatted number: ", wrongNum)
		print("Right contracts percent: ", (rightNum) / len(reportList))


if __name__ == "__main__":
	sc = styleCheck()
	sc.doCheck()
