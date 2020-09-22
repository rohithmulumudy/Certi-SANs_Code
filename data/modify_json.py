# Date: 03/09/2020
# Author: rohith mulumudy
# Description: modifies the json file so that the output json file can be used to parse via python inbuilt functions

import os

def modify_json(in_file, out_file, flag=True):
	f = open(in_file,'r')
	f1 = open(out_file,'w')
	f1.write('[')
	count = 0
	for line in f:
		if count == 1:
			f1.write(',')
		else:
			count = 1

		f1.write(line[:len(line)-1])
	f1.write(']')
	f.close()
	f1.close()
	
	if flag:
		os.system("rm {}".format(in_file))


