# Date: 07/09/2020
# Author: rohith mulumudy
# Description: Removes unreachable domains from the list.

import urllib.request
from urllib.error import HTTPError
import tldextract
import threading

from display import Display

class Preprocessing:
	
	def __init__(self, timeout=10, display_flag=False, display_rate=10, status_redirection="status_redirection.txt", status_code_200="status_code_200.txt",status_code_404="status_code_404.txt",status_others="status_others.txt",status_errors="status_errors.txt"):
		self.status_redirection = status_redirection 
		self.status_code_200 = status_code_200
		self.status_code_404 = status_code_404
		self.status_others = status_others
		self.status_errors = status_errors
		self.timeout = timeout
		self.lock = [threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock(),threading.Lock()]
		self.host_count = 0
		self.display_flag = display_flag
		self.display = Display()
		self.display_rate = display_rate

	def store_response_codes(self, host, status_code):
		self.lock[3].acquire()		
		with open(self.status_others,'a') as fp:
			fp.write("host: {}, status_code: {}\n".format(host,status_code))
		self.lock[3].release()
				
	def store_redirected_hosts(self, orig_host, final_host):
		self.lock[0].acquire()
		with open(self.status_redirection,'a') as fp:
			fp.write("orig_host: {}, final_host: {}\n".format(orig_host,final_host))
		self.lock[0].release()

	def display_progress(self):
		self.lock[5].acquire()
		self.host_count+=1
		if self.host_count%self.display_rate == 0:
			self.display.progress(self.host_count)
		self.lock[5].release()

	def classify_hosts(self, domain):

		try:
			if self.display_flag == True:
				self.display_progress()

			response = urllib.request.urlopen("https://"+domain,timeout=self.timeout)
			response_code = response.getcode()
			request = response.geturl()
			if request:
				ext1 = tldextract.extract(request)
				ext2 = tldextract.extract(domain)
				if(ext1.domain!=ext2.domain):
					store_redirected_hosts(domain,request)

			if response_code == 200:
				self.lock[1].acquire()
				with open(self.status_code_200,'a') as fp:
					fp.write(domain+'\n')
				self.lock[1].release()
					
		except HTTPError as e:
			if e.code == 404:
				self.lock[2].acquire()
				with open(self.status_code_404,'a') as fp:
					fp.write(domain+'\n')
				self.lock[2].release()
				
			elif isinstance(e.code,int):
				store_response_codes(dmn,e.code)
		except:
			self.lock[4].acquire()
			with open(self.status_errors,'a') as fp:
				fp.write(domain+'\n')
			self.lock[4].release()
			
		

