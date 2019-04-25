#!/usr/bin/env python

import paramiko

class pyssh():

	def __init__(self, hostaddress, username):

		self.hostaddress = hostaddress
		self.username = username

	def sshchecker(self):

		client = paramiko.SSHClient()

		client.load_system_host_keys()

		try:

			client.connect(hostname=self.hostaddress,username=self.username)

		except Exception:

			return {'result': 'NOT OK', 'msg': 'Problem with SSH connection to host'}

		else:
			client.close()
			return {'result': 'OK', 'msg': 'No problems detected with SSH connection to host'}


if __name__ == "__main__":

	s = pyssh('192.168.101.203','root')

	print s.sshchecker()	
