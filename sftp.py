import pysftp
cnopts = pysftp.CnOpts(knownhosts='C:\SSH\known_hosts')
with pysftp.Connection(host='', port=22, username='', password='', cnopts=cnopts) as sftp:
    print(sftp.pwd)