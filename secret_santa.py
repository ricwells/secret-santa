############################################
# Secret Santa 2020
# 
# Setup:
# run `cp people.template.json people.json`
# edit people.json with names, exclusions, and email addresses
# be sure to specify "sender_email" before sending emails.
# 
# For details on setting up an email account to use for this program,
# See the tutorial on sending emails with python...
# https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
# 
############################################
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json
import random


def getSantaList(seed=None):
	"""Randomly choose secret santas based on 'people.json'

	Args:
		seed(int): Optional seed for psudo random generator. Use this to have reproducable lists.

	Returns: 
		json: An object containing people with their specified santa person included.
		string: The email address being used to send emails.

	"""

	if(seed is not None):
		random.seed(a=seed)
	with open('people.json') as f:
		data = json.load(f)
		people = data["people"]
		sender = data["sender"]
		for person in people:

			while person["santa"] == None:
				person_index = random.randint(0, (len(people)-1))
				exclusive = False
				for ex in person["exclude"]:
					if ex == people[person_index]["name"]:
						exclusive = True
				if people[person_index]["santee"] == False and exclusive == False:
					person["santa"] = people[person_index]["name"]
					people[person_index]["santee"] = True
		# for person in people:
		# 	print(person)
		return people, sender


def getEmailContents(name, santa, addresses):
	return f"""\
		<html>
			<body>
				<h2>Wells Super Secret Santa</h2>
				<p>Hi {name},<br><br>
					Hope your holiday season is full of joy! 
					It's time to get ready for the Wells secret santa 2020! Yay! 
					Santa's been working hard, and putting together a secret santa program in python. 
					The results are in, and you're secret santa is <b>{santa}</b>!<br>
					As we discussed during the thanksgiving call, If you have any ideas for things 
					you might like from your santa, please send it to all secret santa participants 
					to be sure your santa will get it.<br>
					You can copy and paste the following set of addresses.<br>
					{",".join(addresses)}
				</p>
				<p>
					Curious about this project? Check out <a href="https://github.com/DavidWellsTheDeveloper/secret-santa">the source code</a>.<br> 
					Did you find something wrong with this email? Let Dave know so he can debug the script!
				</p>
			</body>
		</html>
		"""


def sendEmail(people, sender):
	"""For every person specified, send an email to them containing the name of their santa with instructions.

	Args:
		people(json): An object containing people with their specified santa person included. (return value of getSantaList())
		sender(string): The email address being used to send emails.

	"""
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	password = input("Type your password and press enter: ")

	message = MIMEMultipart("alternative")
	message["Subject"] = "Wells Secret Santa!"
	message["From"] = sender

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender, password)
		addresses = []
		for person in people:
			addresses.append(person["email"])
		for person in people:
			santa = person["santa"]
			name = person["name"]
			html = getEmailContents(name, santa, addresses)
			message.attach(MIMEText(html, "html"))
			receiver_email = person["email"]
			message["To"] = person["email"]
			server.sendmail(
				sender, 
				receiver_email, 
				message.as_string()
			)


if __name__ == "__main__":
	people, sender = getSantaList(2020)
	sendEmail(people, sender)
