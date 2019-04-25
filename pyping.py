#!/usr/bin/env python

import subprocess, re, os

class pyping():

	def __init__(self, hostaddress, count, packetsize):

		self.hostaddress = hostaddress
		self.count = str(count)
		self.packetsize = str(packetsize)

	def pingchecker(self):

		f = open('/tmp/pingoutput.txt', 'w')

		subprocess.call(["ping","-c",self.count,"-s",self.packetsize,self.hostaddress], stdout=f , shell=False)

		f.close()

		f = open('/tmp/pingoutput.txt', 'r')

		for line in f:

			search_result = re.search(r'^(\d+) packets transmitted, (\d+) received.*$', line)

			if search_result is not None:

				f.close()
				break

		if search_result.group(1) == search_result.group(2):

			os.remove('/tmp/pingoutput.txt')

			return {'result': 'OK', 'msg': 'No packet drops found'}

		else:

			os.remove('/tmp/pingoutput.txt')

			return {'result': 'NOT OK', 'msg': 'Packet drops detected'}



if __name__ == "__main__":

	p = pyping('192.168.101.202', 5, 1500)

	print p.pingchecker()



