#!/usr/bin/env python
# -*- coding: utf-8 -*-


from urllib2 import Request, urlopen, URLError
from datetime import datetime
import time, os, json, base64, gettext

_ = gettext.gettext

class BitBucketApiException(Exception):
	pass

class BitBucketApi():
	
	def __init__(self):
		self.www = "https://api.bitbucket.org/1.0/"
		
	def __to_datetime(self, timestring):
		return datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
	
	def setLogin(self, user):
		self.user = user
		
	def setPassword(self, pwd):
		self.pwd = pwd
		
	def setOwnerRepo(self, owner):
		self.owner = owner
		
	def setRepoName(self, name):
		self.name = name
	
	def login(self):
		repo = self.www + "repositories/" + self.owner + "/" + self.name + "/"

		credentials = base64.b64encode("{0}:{1}".format(self.user, self.pwd).encode()).decode("ascii")
		headers = {"Authorization": "Basic "+ credentials}
		
		if self.user != "" and self.pwd != "" and self.owner != "" and self.name != "":
			req = Request(repo, None, headers)
			
			try:
				return urlopen(req).read()
			except URLError, e:
				if e.code == 401:
					raise BitBucketApiException(_("Bad login or password"))
				elif e.code == 404:
					raise BitBucketApiException(_("Given bad name of repository/owner"))
			except Exception:
				raise BitBucketApiException(_("An error occured"))
		else:
			raise BitBucketApiException(_("No fields can not be empty"))
			
	def __getLastUpdateDate(self, result):	
		toJson = json.loads(result)
		return toJson['last_updated']

	def checkLastUpdate(self):
		try:
			result = self.login()
			current_date = self.__getLastUpdateDate(result)
			dir = os.getcwd() + "\\data\\"
			path = dir + "revision.txt"
			
			if not os.path.isdir(dir):
				os.makedirs(dir)

			if os.path.exists(path):
				date = open(path, "r").read()
				if(date == current_date):
					return False
				else:
					file = open(path, "w").write(current_date)
					return True
				date.close()
			else:
				open(path, "w").write(current_date)
				return False
		except BitBucketApiException, e:
			return e
            
		