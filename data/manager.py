# Date: 10/09/2020
# Author: rohith mulumudy
# Description: manages the flow of data extraction

import concurrent.futures

from modify_json import modify_json
from get_certificates import Certificates
from preprocessing import Preprocessing
from get_san_domains import San
from file_structure import Files

class Manager:

	def __init__(self, cert_in_file="CAHost.txt", cert_chain_flag=False, thread_count=128,
		 cert_err_file="error_hosts.txt", cert_tmp_file="certs_temp.json", cert_out_file="certs.json", 
		 timeout=10, resume_flag=False, san_file="sans.txt", directory="data_files", display_rate=10, 
		 display_flag=True):

		self.cert_in_file = cert_in_file
		self.cert_chain_flag = cert_chain_flag
		self.thread_count = thread_count
		self.cert_err_file = cert_err_file
		self.cert_out_file = cert_out_file
		self.cert_tmp_file = cert_tmp_file
		self.timeout = timeout
		self.resume_flag = resume_flag
		self.san_file = san_file
		self.directory = directory
		self.display_flag = display_flag
		self.display_rate = display_rate

	def fetch_certificates(self, round_num=1):
		print("\nFetching Certificates...")

		executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count)
			
		err_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_err_file)
		out_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_out_file)
		tmp_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_tmp_file)

		cert = Certificates(self.cert_chain_flag,self.display_flag,self.display_rate,err_file,out_file,tmp_file)

		open(cert.tmp_file,'w').close()
		open(cert.err_file,'w').close()

		hosts = []
		fp = open("{}/{:02d}-round/status_code_200.txt".format(self.directory,round_num))
		for line in fp:
			hosts.append(line.lower().strip())
		fp.close()

		if self.display_flag == True:
			print("Total hosts: {}".format(len(hosts)))
			cert.display.start_progress("Progress",len(hosts))

		for host in hosts:
			executor.submit(cert.get_and_store_certs,host)
		
		executor.shutdown(wait=True)
		modify_json(cert.tmp_file,cert.out_file)

		if self.display_flag == True:
			cert.display.end_progress()

	def resume_fetch_certificates(self, round_num=1):
		print("\nFetching Certificates...")

		executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count)

		err_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_err_file)
		out_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_out_file)
		tmp_file = "{}/{:02d}-round/{}".format(self.directory,round_num,self.cert_tmp_file)
			
		cert = Certificates(self.cert_chain_flag,self.display_flag,self.display_rate,err_file,out_file,tmp_file)

		# getting all domain data
		hosts = []
		fp = open("{}/{:02d}-round/status_code_200.txt".format(self.directory,round_num))
		for line in fp:
			hosts.append(line.lower().strip())
		fp.close()

		# removing half fetched certificate
		try:
			lines = []
			with open(cert.tmp_file) as f:
			    lines = f.read().splitlines() 


			fp = open(cert.tmp_file,'w')
			for line in lines[:-1]:
				fp.write(line)
				fp.write('\n')
			fp.close()

			# getting already fetched domains
			modify_json(cert.tmp_file,cert.out_file,flag=False)

			with open(cert.out_file) as fp:
				data = json.load(fp)

			for line in data:
				hosts.remove(line['host'].lower())

			for line in open(cert.err_file):
				hosts.remove(line.lower().strip())
		
		except FileNotFoundError:
			pass

		if self.display_flag == True:
			print("Total hosts: {}".format(len(hosts)))
			cert.display.start_progress("Progress",len(hosts))

		# execute
		for host in hosts:
			executor.submit(cert.get_and_store_certs,host)
		
		executor.shutdown(wait=True)
		modify_json(cert.tmp_file,cert.out_file)

		if self.display_flag == True:
			cert.display.end_progress()

	###################################################################################
	
	def preprocess(self,round_num=1):
		print("\nPreprocessing...")

		executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count)
		
		status_redirection = "{}/{:02d}-round/redirecton_domains/status_redirection.txt".format(self.directory,round_num)
		status_code_200 = "{}/{:02d}-round/status_code_200.txt".format(self.directory,round_num)
		status_code_404 = "{}/{:02d}-round/unreachable_domains/status_code_404.txt".format(self.directory,round_num)
		status_others = "{}/{:02d}-round/unreachable_domains/status_others.txt".format(self.directory,round_num)
		status_errors = "{}/{:02d}-round/unreachable_domains/status_errors.txt".format(self.directory,round_num)


		hosts = []
		for host in open("{}/{:02d}-round/input/hosts.txt".format(self.directory,round_num)):
			hosts.append(host.strip())

		preprocess = Preprocessing(self.timeout,self.display_flag,self.display_rate,status_redirection,status_code_200,status_code_404,status_others,status_errors)

		if self.display_flag == True:
			print("Total hosts: {}".format(len(hosts)))
			preprocess.display.start_progress("Progress",len(hosts))
		
		for host in hosts:
			executor.submit(preprocess.classify_hosts,host)
		
		executor.shutdown(wait=True)
		
		if self.display_flag == True:
			preprocess.display.end_progress()


	###################################################################################
	
	def get_current_round_domains(self, round_num=1):

		if round_num == 1:
			file = Files(self.directory)
			file.create_file_structure(round_num)
			file.copy_input_file(self.cert_in_file,round_num)
			return True

		in_file = "{}/{:02d}-round/{}".format(self.directory,round_num-1,self.cert_out_file)
		san_file = "{}/{:02d}-round/san_domains/{}".format(self.directory,round_num-1,self.san_file)

		san = San(in_file,san_file)
		san_set = san.get_current_round_sans()

		# hosts
		host_set = set()
		for i in range(1,round_num):
			file = "data_files/{:02d}-round/input/hosts.txt".format(i)
			with open(file) as fp:
				for line in fp:
					host_set.add(line.lower().strip())

		next_round_domains = san_set.difference(host_set)

		if len(next_round_domains) == 0:
			return False

		file = Files(self.directory)
		file.create_file_structure(round_num)
		
		file = "data_files/{:02d}-round/input/hosts.txt".format(round_num)
		with open(file,'w') as fp:
			for dmn in next_round_domains:
				fp.write(dmn+'\n')

		return True

	###################################################################################

	# fetches certificate for a single round
	def manual(self, round_num):

		if not self.get_current_round_domains(round_num):
			return False
		
		print("\n\n------------------ROUND: {} START!!-----------------".format(round_num))

		self.preprocess(round_num)
		if self.resume_flag:
			self.resume_fetch_certificates(round_num)
		else:
			self.fetch_certificates(round_num)

		# print("\n\n------------------ROUND: {} DONE!!------------------".format(round_num))

		return True

	# fetches certificates till no new domains are found
	def automate(self, round_num):
		while self.manual(round_num):
			round_num += 1
		print("\n\n----------------------DONE!!-----------------------")

