# TransferBackup


TransferBackup is a python-based utility for Linux used to perform backups. It checks for the most recent backup file in a folder and transfers the file to the remote machine

It supports email notifications and logging. The logging facility helps you to pinpoint possible reasons for backup failures

## Prerequisites
- This script requires paramiko python library to be installed. You may refer https://www.paramiko.org/installing.html on how to install paramiko
- SSH passwordless login (key-based authentication) must already be configured so that the local machine is able to SSH to the remote machine without a password

## Usage
This script can be used through the CLI

**Options**
```
$ ./TransferBackupScript.py --help
usage: TransferBackupScript.py [-h] --remotehost REMOTEHOST --username USERNAME --remotedirectory REMOTEDIRECTORY --localdirectory LOCALDIRECTORY

Take arguments to transfer backup to remote host

optional arguments:
  -h, --help             show this help message and exit
  --remotehost           REMOTEHOST          IP address of remote host
  --username             USERNAME            user account on remote host
  --remotedirectory      REMOTEDIRECTORY     Directory on remote host
  --localdirectory       LOCALDIRECTORY      Directory on local host
```
<br/>

**Example**

If backup transfer succeeds...

```
$ ./TransferBackupScript.py --remotehost 192.168.101.203 --username root --localdirectory /root/Backup/ --remotedirectory /root/Backup

Checking for packet drops . . .

Checking for SSH conectivity . . .

Backup transfer completed for dbbackup20

$

$ cat /tmp/backup_logfile | tail -25

########## START ##########

[26-05-2019 00:41:39] Starting backup cycle

[26-05-2019 00:41:39] Checking for packet drops . . .

[26-05-2019 00:41:44] No packet drops found

[26-05-2019 00:41:44] Checking for SSH connectivity . . .

[26-05-2019 00:41:44] No problems detected with SSH connection to host

[26-05-2019 00:41:45] Backup transfer completed for dbbackup20


########## END ##########

$

```
<br/>

If backup transfer fails...

```
$ ./TransferBackupScript.py --remotehost 192.168.101.206 --username root --localdirectory /root/Backup/ --remotedirectory /root/Backup


Checking for packet drops . . .

Packet drops detected

Backup transfer aborted

$

$ cat /tmp//backup_logfile | tail -20


########## START ##########

[26-05-2019 02:09:54] Starting backup cycle

[26-05-2019 02:09:54] Checking for packet drops . . .

[26-05-2019 02:10:01] Packet drops detected

[26-05-2019 02:10:01] Backup transfer aborted


########## END ##########

$  
```
<br/>

**Email configuration**

1. To send email notifications to your required email address, you will need to replace the email addresses in send_email() function code with the required email address
2. Replace the "smtp-mail.outlook.com" with the SMTP server address of your email service provider

Below is the code section in TransferBackupScript.py file

```
        def send_email(self, result):

                try:

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

                except Exception:

                        self.logfile_object.write(self.timestamp_generator() + " " + "An email could not be sent\n\n")

```
