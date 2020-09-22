# Date: 09/09/2020
# Author: rohith mulumudy
# Description: stores san domain data.		

import json

class San:

	def __init__(self, in_file="certs.json", san_file="sans.txt"):
		self.in_file = in_file
		self.san_file = san_file

	def get_san_lst(self, san):
		lst = []
		temp = san.split(';')
		for i in range(len(temp)):
			if(temp[i].find(":")<0):
				continue
			if '*' not in temp[i]:
				lst.append(temp[i].split(':')[1].lower())
			else:
				lst.append(temp[i].split(':')[1][2:].lower())
		return lst

	# Given round number, stores san from the given round certs 
	def store_sans(self):
		with open(self.in_file) as fp:
			data = json.load(fp)

		with open(self.san_file,'w') as fp:			
			for i in range(len(data)):
				san = data[i]['certificate']['san']
				lst = self.get_san_lst(san)
				
				for dmn in lst:
					fp.write(dmn+'\n')
	
	def edit_san_file(self):
		san_set = set()

		with open(self.san_file) as fp:
			for line in fp:
				san_set.add(line.strip())

		with open(self.san_file,'w') as fp:
			for dmn in san_set:
				fp.write(dmn+'\n')

		return san_set

	def get_current_round_sans(self):

		self.store_sans()
		return self.edit_san_file()