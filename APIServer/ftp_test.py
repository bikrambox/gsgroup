import ftplib
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ftp = ftplib.FTP_TLS(context=context, timeout=1200)
ftp.connect('10.6.8.43', 21)
ftp.login('BHSR\\jeba', 'Hundekoldt2006!')
ftp.prot_p()
ftp.set_pasv(True)
print("Connected successfully")
ftp.quit()