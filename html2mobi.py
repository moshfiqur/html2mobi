import requests
from readability import Document
import re
from subprocess import call
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# Get the html
response = requests.get("http://URL/TO/CONVERT")

# Clean up the html using readability
doc = Document(response.text)

# Use the webpage title as base file name
file_name = re.sub(r'[^a-zA-Z0-9]+', '-', doc.title())

# Write the html response to local file
f = open(file_name + '.html', 'w')
f.write(doc.summary())
f.close()

# Convert the local html file to .mobi
call(["./kindlegen", file_name + '.html'])

# Send the document as email attachment
msg = MIMEMultipart()
send_from = msg['From'] = 'from@email.address'
send_to = msg['To'] = 'to@email.address' # Can be 'Send to Kindle' email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = file_name + ".mobi"

# Attache email body
msg.attach(MIMEText('Want to write a customized email boddy? Then put it here.'))

# Attach the .mobi file
fp = open(file_name + ".mobi", "rb")
mobi_file = MIMEApplication(fp.read())
fp.close()
encoders.encode_base64(mobi_file)
mobi_file.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name + '.mobi')
msg.attach(mobi_file)

# Send the email
smtp = smtplib.SMTP("smtp_server:port")
smtp.starttls()
smtp.login('smtp_username', 'smtp_password')
smtp.sendmail(send_from, send_to, msg.as_string())
smtp.quit()
