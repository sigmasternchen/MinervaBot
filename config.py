CONSUMER_KEY = 'Your Twitter API Consumer Key'
CONSUMER_SECRET = 'Your Consumer Secret Key'
ACCESS_TOKEN_KEY = 'Your Twitter API Access Token Key'
ACCESS_TOKEN_SECRET = 'Your Access Token Secret'

# empty array for no mention
# else add comma-separated, quote-enclosed twitter names with @
DESTINATION_ACCOUNTS = []
WARNING_DESTINATION_ACCOUNTS = []

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
	#"mdstat:": 'cat /proc/mdstat | grep block | sed "s/\s\+/ /g"',
	#"lxc:": 'lxc-ls -f -F name,state | grep -v "NAME" | grep -v "\-" | sed "s/\s\+/ /g" | sed "s/ /: /"| sed "s/RUNNING/UP/" | sed "s/STOPPED/DOWN/"',
	"df:": "df -h --output=source,size,used | grep /dev/ | sed 's/\s\+/ /g'",
	"ping:" 'ping -c1 8.8.8.8 | grep from | awk -F"time=" \'{ print $2 }\''
}

WARNING_COMMANDS = {
	#"mdadm:": [
	#	"cat /proc/mdstat | grep block | awk -F'[' '{ print $3 }' | awk -F']' '{ print $1 }'", 
	#	"UUU", 
	#	"RAID has a problem!"
	#],
	"hddtemp:": [
		"hddtemp /dev/sd* | awk '{ print $(NF-1) }' | while read val; do if test $val -gt 50; then echo HOT; break; fi; done", 
		"", 
		"1 or more HDDs are too hot!"
	]
}
