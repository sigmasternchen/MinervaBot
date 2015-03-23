import tweepy
import sys
import datetime
import time

from subprocess import Popen, PIPE, STDOUT

ACCESS_TOKEN_KEY = "holder"

from config import *
from genconfig import *

logfile = open(LOG_FILE, LOG_TYPE)

def log(text):
	logfile.write(datetime.datetime.now().isoformat() + ": " + text + "\n")
	print(datetime.datetime.now().isoformat() + ": " + text)

def connect():
	global ACCESS_TOKEN_KEY
	global ACCESS_TOKEN_SECRET
	auth = tweepy.OAuthHandler(
		consumer_key = CONSUMER_KEY,
		consumer_secret = CONSUMER_SECRET
	)
	if USE_PIN_AUTH:
		if ACCESS_TOKEN_KEY == "holder":
			print("auth url: " + auth.get_authorization_url())
			pin = input("pin: ").strip()
			token = auth.get_access_token(
				verifier = pin
			)
			genconf = open("genconfig.py", "w")
			genconf.write("# don't edit this file\n\n")
			genconf.write("ACCESS_TOKEN_KEY = '" + token[0] + "'\n")
			genconf.write("ACCESS_TOKEN_SECRET = '" + token[1] + "'\n")
			genconf.close()

			ACCESS_TOKEN_KEY = token[0]
			ACCESS_TOKEN_SECRET = token[1]
	else:
		ACCESS_TOKEN_KEY = NP_ACCESS_TOKEN_KEY
		ACCESS_TOKEN_SECRET = NP_ACCESS_TOKEN_SECRET

	auth.secure = True
	auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)
	
	if not api.verify_credentials():
		print("error! auth failed.")
		sys.exit(1)
	else:
		return api
		


if __name__ == "__main__":

	log("starting minerva")

	api = connect()
	log("connected to Twitter API")

	counter = 0

	lastChangeT  = 0
	lastChangeDM = 0

	lastChangeDM = api.direct_messages()
	if len(lastChangeDM) == 0:
		lastChangeDM = 0
	else: 
		lastChangeDM = lastChangeDM[0].GetId()
	lastChangeT = api.mentions_timeline()
	if len(lastChangeT) != 0:
		lastChangeT = lastChangeT[0].GetId()

	while True:
		if ALLOW_COMMANDS:
			dms = api.direct_messages(since_id = lastChangeDM)
			
			commandsToExecute = []
			for dm in dms:
				lastChangeDM = dm.id
				if len(COMMAND_SOURCE_ACCOUNTS) == 0:
					commandsToExecute.append([
						dm.GetSenderScreenName(), 
						dm.GetText()
					])
				else:
					for user in COMMAND_SOURCE_ACCOUNTS:
						if dm.author.screen_name == user:
							commandsToExecute.append([
								dm.author.screen_name, 
								dm.text
							])
						else:
							log("unprivileged user @" + dm.author.screen_name + " tried to execute command (dm) \"" + dm.text.replace("\n", "\\n") + "\"")

			if not ALLOW_ONLY_DM_COMMANDS:
				mentions = api.mentions_timeline(since_id = lastChangeT)
				for mention in mentions:
					lastChangeT = mention.id
					if len(COMMAND_SOURCE_ACCOUNTS) == 0:
						commandsToExecute.append([
							mention.author.screen_name,
							mention.text
						])
					else:
						for user in COMMAND_SOURCE_ACCOUNTS:
							if mention.author.screen_name == user:
								commandsToExecute.append([
									mention.author.screen_name,
									mention.text
								])
							else:
								log("unprivileged user @" + mention.author.screen_name + " tried to execute command \"" + mention.text.replace("\n", "\\n") + "\"")

		
			for command in commandsToExecute:
				log("executing command (@" + command[0] + ") \"" + command[1].replace("\n", "\\n") + "\"")
				output = Popen(command[1], shell=True, stdout=PIPE, stderr=STDOUT).stdout.read().decode("utf-8")
				log("result: " + output);
				if (output + command[0]).len() + 2 > 140:
					api.update_status(status = (command[0] + "Output of command is too long. I'm sry. : /"))
				else:
					api.update_status(status = (command[0] + " " + output))
	

		for command in UPDATE_COMMANDS:
			output = Popen(UPDATE_COMMANDS[command], shell=True, stdout=PIPE, stderr=STDOUT).stdout.read().decode("utf-8")
			if len(DESTINATION_ACCOUNTS):
				for username in DESTINATION_ACCOUNTS:
					api.update_status(status = (username + " " + command + COMMAND_NAME_SEPERATOR + output))
			else:
				api.update_status(status = (command + COMMAND_NAME_SEPERATOR + output))

	
		if counter % 3 == 0:
			for command in WARNING_COMMANDS:
				output = Popen(WARNING_COMMANDS[command][0], shell=True, stderr=STDOUT, stdout=PIPE).stdout.read().decode("utf-8")
				if output != WARNING_COMMANDS[command][1]:
					if len(WARNING_DESTINATION_ACCOUNTS):
						for username in WARNING_DESTINATION_ACCOUNTS:
							api.update_status(status = (username + " WARNING: " + command + COMMAND_NAME_SEPERATOR + WARNING_COMMANDS[command][2]))
					else:
						api.update_status(status = ("WARNING: " + command + COMMAND_NAME_SEPERATOR + WARNING_COMMANDS[command][2]))
		time.sleep(5 * 60)

		counter += 1
