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

	# Module - Bridgey
	"bridgey": {
		# Enable bridging
		# type: bool
		"enabled": False,

		# List of pools (don't change pools and platforms name after you start the bridge)
		# type: dict[str, dict[str, dict]]
		"pools": {
			"example": {
				"discord": {
					# The name of the platform
					# type: str
					"platform": "Discord",

					# ID of the channel to bridge
					# type: int
					"channel_id": 0,

					# Bot token
					# type: str
					"token": "",
				},

				"matrix": {
					# The name of the platform
					# type: str
					"platform": "Matrix",

					# User ID of the bot account (e.g. @user:matrix.org)
					# type: str
					"username": "",

					# Password of the bot account
					# type: str
					"password": "",

					# URL of the Matrix server (e.g. https://matrix.org)
					# type: str
					"homeserver_url": "",

					# The alias of the room you want to bridge (e.g. #room:matrix.org)
					# type: str
					"room_alias": "",
				},

				"telegram": {
					# The name of the platform
					# type: str
					"platform": "Telegram",

					# ID of the chat to bridge
					# type: int
					"chat_id": 0,
				},
			},
		},
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
