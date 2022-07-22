config = {
	# [START]
	"bot": {
		# Add here your HTTP API bot token, get it from @BotFather
		# type: str
		"api_token": "",

		# Logging channel/group ID, exceptions will be sent there
		# type: int | str
		"logging_chat_id": "",
	},

	# Module - LineageOS updates
	"lineageos_updates": {
		# type: bool
		"enable": False,

		# type: str
		"chat_id": "",
	},

	# Library - libadmin
	"libadmin": {
		# type: list[int]
		"admin_user_ids": [],

		# type: list[int]
		"approved_user_ids": [],
	},
	# [END]
}
