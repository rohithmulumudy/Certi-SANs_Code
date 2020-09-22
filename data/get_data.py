# Date: 22/09/2020
# Author: rohith mulumudy
# Description: calls manager, by reading all the constants from configuration file

from platform import python_version

from manager import Manager
from configurations import *


if __name__ == '__main__':

    # start_time = time.time()

    if int(python_version()[0]) < 3:
        print('[!] Please use Python 3')
        exit()

    manager = Manager(cert_in_file,cert_chain_flag,thread_count,cert_err_file,
				cert_tmp_file,cert_out_file,timeout,resume_flag,san_file,directory,display_rate,display_flag)
    manager.automate(1)

    # print('\n Time elapsed: ', (time.time() - start_time), ' seconds')