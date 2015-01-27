import twitter
import sys
import subprocess
import datetime
import time

from config import *

logfile = open(LOG_FILE, LOG_TYPE)

def log(text):
	logfile.write(datetime.datetime.now().isoformat() + ": " + text))

def connect():
	return twitter.Api(
		consume_key = CONSUMER_KEY,
		consumer_secret = CONSUMER_SECRET,
		access_token_key = ACCESS_TOKEN_KEY,
		access_token_secret = ACCESS_TOKEN_SECRET
	)


if __name__ == "__main__":

	log("starting minerva")

	api = connect()
	log("connected to Twitter API")

	lastChange = 0

	lastChange = api.getDirectMessages(since_id = lastChange)[0].GetId()
	lastChange = api.getMentions(since_id = lastChange)[0].GetId()

	while true:
		if ALLOW_COMMANDS:
			dms = api.getDirectMessages(since_id = lastChange)
			
			commandsToExecute = []
			for dm in dms:
				if len(COMMAND_SOURCE_ACCOUNTS) == 0:
					commandsToExecute.append([
						dm.GetSenderScreenName(), 
						dm.GetText()
					])
				else:
					for user in COMMAND_SOURCE_ACCOUNTS:
						if dm.GetSenderScreenName() == user:
							commandsToExecute.append([
								dm.GetSenderScreenName(), 
								dm.GetText()
							])
						else:
							log("unprivileged user @" + dm.GetSenderScreenName() + " tried to execute command (dm) \"" + dm.GetText().replace("\n", "\\n") + "\"\n")

			if not ALLOW_ONLY_DM_COMMANDS:
				mentions = api.GetMentions(since_id = lastChange)
				for mention in mentions:
					if len(COMMAND_SOURCE_ACCOUNTS) == 0:
						commandsToExecute.append([
							mention.GetUser().GetScreenName(), 
							mention.GetText()
						])
					else:
						for user in COMMAND_SOURCE_ACCOUNTS:
							if mention.GetUser().GetScreenName() == user:
								commandsToExecute.append([
									mention.GetUser().GetScreenName(),
									mention.GetText()
								])
							else:
								log("unprivileged user @" + mention.GetUser().GetScreenName() + " tried to execute command \"" + mention.GetText().replace("\n", "\\n") + "\"\n")

		
			for command in commandsToExecute:
				log("executing command (@" + command[0] + ") \"" + command[1].replace("\n", "\\n") + "\"")
				output = subprocess.Popen(command[1], shell=True, stdout=PIPE).stdout.read()
				log("result: " + output);
				if (output + command[0]).len() + 2 > 140:
					api.PostUpdate(status = command[0] + "Output of command is too long. I'm sry. : /")
				else:
					api.PostUpdate(status = command[0] + " " + output)
	

		for command in UPDATE_COMMANDS:
			output = subprocess.Popen(UPDATE_COMMANDS[command], shell=True, stdout=PIPE).stdout.read()
			api.PostUpdate(status = (command + COMMAND_NAME_SEPERATOR + output))

	
		time.sleep(5 * 60) 

