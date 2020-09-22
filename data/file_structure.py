# Date: 10/09/2020
# Author: rohith mulumudy
# Description: manages the file structure

import os

class Files:

	def __init__(self, directory):
		self.directory = directory

	def create_file_structure(self, round_num):

		if not os.path.isdir(self.directory):
			os.mkdir(self.directory)

		if not os.path.isdir("{}/{:02d}-round".format(self.directory,round_num)):
			os.mkdir("{}/{:02d}-round".format(self.directory,round_num))

		if not os.path.isdir("{}/{:02d}-round/redirection_domains".format(self.directory,round_num)):
			os.mkdir("{}/{:02d}-round/redirection_domains".format(self.directory,round_num))

		if not os.path.isdir("{}/{:02d}-round/unreachable_domains".format(self.directory,round_num)):
			os.mkdir("{}/{:02d}-round/unreachable_domains".format(self.directory,round_num))

		if not os.path.isdir("{}/{:02d}-round/san_domains".format(self.directory,round_num)):
			os.mkdir("{}/{:02d}-round/san_domains".format(self.directory,round_num))

		if not os.path.isdir("{}/{:02d}-round/input".format(self.directory,round_num)):
			os.mkdir("{}/{:02d}-round/input".format(self.directory,round_num))


		open("{}/{:02d}-round/redirection_domains/status_redirection.txt".format(self.directory,round_num),'w').close()
		open("{}/{:02d}-round/status_code_200.txt".format(self.directory,round_num),'w').close()
		open("{}/{:02d}-round/unreachable_domains/status_code_404.txt".format(self.directory,round_num),'w').close()
		open("{}/{:02d}-round/unreachable_domains/status_others.txt".format(self.directory,round_num),'w').close()
		open("{}/{:02d}-round/unreachable_domains/status_errors.txt".format(self.directory,round_num),'w').close()
		

	def copy_input_file(self, in_file, round_num):
		os.system("cp {} {}/{:02d}-round/input/hosts.txt".format(in_file,self.directory,round_num))

