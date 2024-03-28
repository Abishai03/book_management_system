import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders


filename = "filename.pdf"
receivers = [""]
subject= "Purchased Book"

server = smtplib.SMTP('smtp.gmail.com', 587)

message = MIMEMultipart()
message["From"] = "Book Management"
message['To'] = '_'.join(receivers)
message["Subject"] = subject

with open(filename, "rb") as attachment:
	part = MIMEBase("application", "octet-stream")
	part.set_payload(attachment.read())
	encoders.encode_base64(part)

part.add_header(
"Content-Disposition",
f"attachment; filename= {filename}",
)

html = """\
<p>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
</p>
html body
"""
message.attach(part)
message.attach(MIMEText(html, "html"))
message = message.as_string()
# start TLS for security user_to
server.starttls()

# Authentication 
server.login("user", "password")
sender = "email"

try:
	server.sendmail(sender, receivers, message)
except Exception as e:
	raise e