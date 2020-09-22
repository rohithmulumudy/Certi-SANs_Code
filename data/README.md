# HTTPS Cetificate extraction

An automated recursive multi-threaded code for downloading HTTPS certificates. Made with python.

## Requirements

Python v3

## External Dependencies
-	urllib
-	tldextract
-	OpenSSL

## Usage

    python3 get_data.py

## Description

The run time parmeters (including number of threads) can be set in configurations.py file.

The certificates are fetched for the domains mentioned in **cert_in_file** (can be found in configurations.py file). For reference see: [sample input file](sample.txt)

The output folder format can be seen [here](#File-Structure)

The code recursively fetches the certificate from the domains in the **Subject Alternative Name** field until no new domains are found.

If you want to use non recursive approach, use the **manual** method in the **Manager** class.

## File Strucutre

```
data_files
└── 'i'-round (i = 01,02,03,...)
    ├── unreachable_domain
    │	├── status_code_404.txt
	│	├──	status_others.txt
	│	└──	status_errors.txt
    ├── redirection_domains
    │	└── status_redirection.txt
	├── san_domains
	│	└── sans.txt # The san domains obtained from cert.json
	├── input
	│	└── hosts.txt # The domains file used for fetching certs
    ├ status_code_200.txt
    ├ certs.json # certificate file
    ├ certs_temp.json # intermediate file - can be seen only if some error occurs
    └ error_hosts.txt
```