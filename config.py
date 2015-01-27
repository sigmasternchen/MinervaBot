CONSUMER_KEY = 'Your Twitter API Consumer Key'
CONSUMER_SECRET = 'Your Consumer Secret Key'
ACCESS_TOKEN_KEY = 'Your Twitter API Access Token Key'
ACCESS_TOKEN_SECRET = 'Your Access Token Secret'

# add @ to account name
# leave empty for no mention
DESTINATION_ACCOUNT = ''
DESTINATION_ACCOUNT_IMPORTANT = ''

ALLOW_COMMANDS = false
ALLOW_ONLY_DM_COMMANDS = false

# empty array for everyone
# else add comma-separated, quote-enclosed twitter names with @
COMMAND_SOURCE_ACCOUNTS = []

# use "w" for overwrite, or "a" for append
LOG_TYPE = "a"
LOG_FILE = "~/minerva.log"

COMMAND_NAME_SEPERATOR = "\n"

UPDATE_COMMANDS = {
	"uptime:": "uptime",
	"mdstat:": 'cat /proc/mdstat | grep block | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /"',
	"lxc:": 'lxc-ls -f -F name,state | grep -v "NAME" | grep -v \- | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/ /: /" | sed "s/RUNNING/UP/" | sed "s/STOPPED/DOWN/"',
	"df:": 'df -h --output=source,size,used | grep /dev/ | grep -v tmpfs | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /" | sed "s/  / /"',
	"ping:" 'ping -c1 8.8.8.8 | grep from | awk -F"time=" \'{ print $2 }\''
}
