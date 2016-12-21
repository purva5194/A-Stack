import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('127.0.0.1',port=2230, username='osbash', password='osbash')
except paramiko.SSHException:
    print "Connection Failed"
    quit()

stdin, stdout, stderr = ssh.exec_command("bash sc.sh")

for line in stdout.readlines():
    print line.strip()
ssh.close()