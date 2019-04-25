#!/usr/bin/env python

from pyping import pyping
from pyssh import pyssh
from datetime import datetime
import os, sys, subprocess, smtplib

class Backup:

	def __init__(self, remotehost, username, localdirectory, remotedirectory):

		self.remotehost = remotehost
		self.username = username
		self.localdirectory = localdirectory
		self.remotedirectory = remotedirectory
		self.logfile_object = open('/tmp/backup_logfile', 'a')


	def ping_check(self):

		d = datetime.now()
		current_ts = d.strftime("%d-%m-%Y %H:%M:%S")

		self.logfile_object.write("########## START ##########\n\n")
		self.logfile_object.write(self.timestamp_generator() + " Starting backup cycle" + "\n\n")

		print "\n\nChecking for packet drops . . .\n\n"
		self.logfile_object.write(self.timestamp_generator() + " Checking for packet drops . . .\n\n")

		ping_check_result = pyping(self.remotehost, 5, 1500).pingchecker()
		self.logfile_object.write(self.timestamp_generator() + " " + ping_check_result['msg'] + "\n\n")

		if ping_check_result['result'] != 'OK':

			self.logfile_object.write(self.timestamp_generator() + " Backup transfer aborted\n\n")
			self.logfile_object.write("########## END ##########\n\n\n\n\n")
			self.logfile_object.close()
			self.send_email('Backup failed')
			sys.exit(0)


	def ssh_check(self):

		print "\n\nChecking for SSH conectivity ...\n\n"
		self.logfile_object.write(self.timestamp_generator() + " Checking for SSH connectivity . . .\n\n")

		ssh_check_result = pyssh(self.remotehost,self.username).sshchecker()
		self.logfile_object.write(self.timestamp_generator() + " " + ssh_check_result['msg'] + "\n\n")

		if ssh_check_result['result'] != 'OK':

			self.logfile_object.write(self.timestamp_generator() + " Backup transfer aborted in SSH check\n\n")
			self.logfile_object.write("########## END ##########\n\n\n\n\n")
			self.logfile_object.close()
			self.send_email('Backup failed')
			sys.exit(0)

	def timestamp_generator(self):

		d = datetime.now()
		return (d.strftime("[%d-%m-%Y %H:%M:%S]"))


	def filetransfer(self):

		find_last_backup_file = subprocess.call("ls -1t %s | head -1" %(self.localdirectory), stdout=open('/tmp/tmpfile01', 'w'), shell=True)
	
		fd_tmpfile01 = open('/tmp/tmpfile01', 'r')	
		latest_backup_file = (fd_tmpfile01.read()).rstrip()

		absolute_file_path = self.localdirectory + latest_backup_file

		transfer_file = subprocess.call("rsync -avzhe ssh %s %s@%s:%s" %(absolute_file_path, self.username, self.remotehost, self.remotedirectory), stdout=open('/tmp/tmpfile02', 'w'), shell=True)

		if transfer_file == 0:

			self.logfile_object.write(self.timestamp_generator() + " Backup transfer completed\n\n")
			self.logfile_object.write("########## END ##########\n\n\n\n\n")
			self.logfile_object.close()
			self.send_email('Backup successful')

		else:

			self.logfile_object.write(self.timestamp_generator() + " Backup transfer failed\n\n")
			self.logfile_object.write("########## END ##########\n\n\n\n\n")
			self.logfile_object.close()
			self.send_email('Backup failed')


	def tmp_files_cleanup(self):

		os.remove('/tmp/tmpfile01')
		os.remove('/tmp/tmpfile02')


	def send_email(self, result):

		s = smtplib.SMTP('smtp-mail.outlook.com', 587)

		s.starttls()

		s.login('youremail@email.com', 'password')

		frm = 'youremail@email.com'
		to = 'youremail@email.com'
		subject = 'Backup status'
		body = result

		msg = "From: <%s>\nTo: <%s>\nSubject: %s\n\n%s\n\n" %(frm,to,subject,body)

		s.sendmail(frm,to,msg)

		s.close()

b = Backup('192.168.101.203', 'root', '/root/Backup/', '/root/Backup/')

b.ping_check()

b.ssh_check()

b.filetransfer()

b.tmp_files_cleanup()


