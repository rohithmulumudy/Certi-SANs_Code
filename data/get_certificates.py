# Date: 03/09/2020
# Author: rohith mulumudy
# Description: fetches certificate data 

import socket
from OpenSSL import SSL
from OpenSSL import crypto
from ssl import PROTOCOL_TLSv1
import json
import socks
from datetime import datetime
import threading

from display import Display


class Certificates:

	def __init__(self, cert_chain_flag=False, display_flag=False, display_rate=10, err_file="error_hosts.txt", out_file="certs.json", tmp_file="certs_temp.json"):
		
		self.lock = threading.Lock()
		self.port = "443"
		self.cert_chain_flag = cert_chain_flag
		self.err_file = err_file
		self.out_file = out_file
		self.tmp_file = tmp_file
		self.host_count = 0
		self.display_flag = display_flag
		self.display = Display()
		self.display_rate = display_rate

	def get_cert_sans(self, x509cert):
	    
	    san = ''
	    ext_count = x509cert.get_extension_count()
	    for i in range(0, ext_count):
	        ext = x509cert.get_extension(i)
	        if 'subjectAltName' in str(ext.get_short_name()):
	            san = ext.__str__()
	    # replace commas to not break csv output
	    san = san.replace(',', ';')
	    return san

	def get_cert_details(self, cert):
		context = {}
		issuer={}
		subject = {}

		issuer['countryName'] = cert.get_issuer().C
		issuer['stateOrProvinceName'] = cert.get_issuer().ST
		issuer['localityName'] = cert.get_issuer().L
		issuer['organizationName'] = cert.get_issuer().O
		issuer['organizationUnitName'] = cert.get_issuer().OU
		issuer['commonName'] = cert.get_issuer().CN
		issuer['emailAddress'] = cert.get_issuer().emailAddress

		context['issuer'] = issuer
		
		context['serialNumber'] = str(cert.get_serial_number())
		context['signatureAlgorithm'] = cert.get_signature_algorithm().decode()

		subject['countryName'] = cert.get_subject().C
		subject['stateOrProvinceName'] = cert.get_subject().ST
		subject['localityName'] = cert.get_subject().L
		subject['organizationName'] = cert.get_subject().O
		subject['organizationUnitName'] = cert.get_subject().OU
		subject['commonName'] = cert.get_subject().CN
		subject['emailAddress'] = cert.get_subject().emailAddress

		context['subject'] = subject
		context['version'] = cert.get_version()
		context['subjectNameHash'] = cert.subject_name_hash()
		context['san'] = self.get_cert_sans(cert)
		context['expired'] = cert.has_expired()
		

		# Valid from
		valid_from = datetime.strptime(cert.get_notBefore().decode('ascii'),
		                               '%Y%m%d%H%M%SZ')
		context['valid_from'] = valid_from.strftime('%Y-%m-%d')

		# Valid till
		valid_till = datetime.strptime(cert.get_notAfter().decode('ascii'),
		                               '%Y%m%d%H%M%SZ')
		context['valid_till'] = valid_till.strftime('%Y-%m-%d')

		# Validity days
		context['validity_days'] = (valid_till - valid_from).days

		# Validity in days from now
		now = datetime.now()
		context['days_left'] = (valid_till - now).days

		return context

	def get_certs(self, host):
		# socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, '172.16.2.30', 8080, True)
		socket.socket = socks.socksocket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		osobj = SSL.Context(PROTOCOL_TLSv1)
		try:
			sock.connect((host, int(self.port)))
			oscon = SSL.Connection(osobj, sock)
			oscon.set_tlsext_host_name(host.encode())
			oscon.set_connect_state()
			oscon.do_handshake()
			if self.cert_chain_flag:
				certs = oscon.get_peer_cert_chain()
			else:
				certs = oscon.get_peer_certificate()
			sock.close()
			return certs
		except:
			return 0

			
	def store_certs(self, host, cert, fp):
		
		data = {}
		
		data['host'] = host
		data['certificate'] = self.get_cert_details(cert)

		fp.write(json.dumps(data))
		fp.write('\n')


	def store_cert_chain(self, host, certs, fp):
		data = {}

		data['host'] = host

		data['certificate'] = {}
		for i,cert in enumerate(certs):
			data['certificate'][i+1] = self.get_cert_details(cert)


		fp.write(json.dumps(data))
		fp.write('\n')


	def display_progress(self):
		self.host_count+=1
		if self.host_count%self.display_rate == 0:
			self.display.progress(self.host_count)

	def get_and_store_certs(self, host):
		cert = self.get_certs(host)
				
		self.lock.acquire()
		# print(threading.current_thread().getName())

		try:

			if self.display_flag == True:
				self.display_progress()

			with open(self.tmp_file,'a') as fp:
				if self.cert_chain_flag:
					self.store_cert_chain(host,cert,fp)
				else:
					self.store_certs(host,cert,fp)
		except:
			with open(self.err_file,'a') as fp:
				fp.write(host+'\n')
		finally:
			self.lock.release()

