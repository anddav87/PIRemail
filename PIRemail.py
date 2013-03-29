import RPi.GPIO as GPIO
import time
import sys
import os



#Set the GPIO pin (board numbering) for the PIR

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

while True:
  ir_val = GPIO.input(11)
  if not ir_val:
  	time.sleep(0.5)
  elif ir_val:
  	print "Alarm"
  	## {{{ http://code.activestate.com/recipes/473810/ (r1)
  	# Send an HTML email with an embedded image and a plain text message for
  	# email clients that don't want to display the HTML.
  	
    # this assumes you have a fswebcam configuration file, just use fswebcam otherwise
  	os.system("fswebcam -c fswebcam.conf webcam.jpg")

  	from email.MIMEMultipart import MIMEMultipart
  	from email.MIMEText import MIMEText
  	from email.MIMEImage import MIMEImage

  	# Define these once; use them twice!
  	strFrom = 'username@googlemail.com'
  	strTo = 'receiveremail@domain.com'

  	# Create the root message and fill in the from, to, and subject headers
  	msgRoot = MIMEMultipart('related')
  	msgRoot['Subject'] = 'Latest PIR Webcam Pic from Rasp Pi'
  	msgRoot['From'] = strFrom
  	msgRoot['To'] = strTo
  	msgRoot.preamble = 'This is a multi-part message in MIME format.'

  	# Encapsulate the plain and HTML versions of the message body in an
  	# 'alternative' part, so message agents can decide which they want to display.
  	msgAlternative = MIMEMultipart('alternative')
  	msgRoot.attach(msgAlternative)

  	msgText = MIMEText('This is the alternative plain text message.')
  	msgAlternative.attach(msgText)

  	# We reference the image in the IMG SRC attribute by the ID we give it below
  	msgText = MIMEText('Here is the latest PIR Trigger webcam pic: <br><img src="cid:image1"><br>', 'html')
  	msgAlternative.attach(msgText)

  	# This example assumes the image is in the current directory
  	fp = open('webcam.jpg', 'rb')
  	msgImage = MIMEImage(fp.read())
  	fp.close()

  	# Define the image's ID as referenced above
  	msgImage.add_header('Content-ID', '<image1>')
  	msgRoot.attach(msgImage)

  	# Send the email (this example assumes SMTP authentication is required)
  	import smtplib
  	smtp = smtplib.SMTP()
  	smtp.connect('smtp.gmail.com')
  	smtp.starttls()
  	smtp.login('username', 'password')
  	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
  	smtp.quit()
  	## end of http://code.activestate.com/recipes/473810/ }}}
  	while ir_val:
  		ir_val = GPIO.input(11)
  		time.sleep(0.5)
  else:
  	print "Error"
  	
 


