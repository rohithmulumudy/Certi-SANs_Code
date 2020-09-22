# Date: 10/09/2020
# Author: rohith mulumudy
# Description: contains configuration data. 	
	# Check the keys which are tagged "Important" before execution. #Important

## Certificate Fetching Constants

### Contains domains list 
cert_in_file = "sample.txt" #important

### File that stores domains which threw error while fetching certificates
cert_err_file = "error_hosts.txt"

### File that stores certifcate data
cert_out_file = "certs.json" # should be a json file

### File that temporarily stores certificate data (before parsing)
cert_tmp_file = "certs_temp.json"

### If True gets the certificate chain data else gets the end user certificate
cert_chain_flag = False

### If True coninues from where it stopped else starts the execution freshly
resume_flag = False # Important

########################################################################################

## Preporcessing

### urllib timeout
timeout = 10 # Important

########################################################################################

## get_san_domains

### File that stores san domains
san_file = "sans.txt"

########################################################################################

## General

### Optimal value for a 4 core machine any value >= 64 
thread_count = 128 # Important

### Directory
directory = "data_files"

### display flag
display_flag = True # Important

### refreshes display after the specified amount of hosts are processed
display_rate = 100