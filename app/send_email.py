import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import dotenv_values
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()


gmail_user = os.getenv('email')
gmail_password = os.getenv('password')


def send_book(files=None, recipient=None, content=None):
	# Create message container
	msg = MIMEMultipart()
	msg['From'] = gmail_user
	msg['To'] = recipient  # Replace with recipient's email
	msg['Subject'] = 'Subject of the Email'

	# Email body
	body = content
	msg.attach(MIMEText(body, 'html'))
	if files:
		for file in files:
			# Attach file
			attachment = open("app/"+file, 'rb')
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % file.split("/")[-1])
			msg.attach(part)

	try:
		# Establish a connection to Gmail's SMTP server
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		# Login to Gmail
		server.login(gmail_user, gmail_password)
		# Send Email
		server.sendmail(gmail_user, msg['To'], msg.as_string())
		# Close the connection
		server.close()
		print('Email sent successfully!')
		return 1
	except Exception as e:
		print('Something went wrong...', e)
		return 0
# send_book("static/uploads/book-cover.jpeg", "azizu7166@gmail.com", "content")
