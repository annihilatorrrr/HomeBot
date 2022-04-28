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

	# Module - CI
	# Read this before continuing: https://github.com/SebaUbuntu/HomeBot/wiki/Modules-%7C-ci#variables
	"ci": {
		# type: str
		"main_dir": "",

		# type: str
		"channel_id": "",

		# type: bool
		"upload_artifacts": False,

		# type: str
		"github_username": "",

		# type: str
		"github_token": "",

		# type: bool
		# Enable ccache
		"enable_ccache": False,

		# type: str
		# Path to ccache executable
		"ccache_exec": "",

		# type: str
		# Path to ccache files
		"ccache_dir": "",

		# twrpdtgen script
		"twrpdtgen": {
			# type: str
			"github_org": "",

			# type: str
			"channel_id": "",
		}
	},

	# Module - LineageOS updates
	"lineageos_updates": {
		# type: bool
		"enable": False,

		# type: str
		"chat_id": "",
	},

	# Module - Translate
	"translate": {
		# type: str
		# DeepL API key
		"deepl_api_key": "",
	},

	# Library - libadmin
	"libadmin": {
		# type: list[int]
		"admin_user_ids": [],

		# type: list[int]
		"approved_user_ids": [],
	},

	# Library - libupload
	"libupload": {
		"default": {
			# type: str
			"method": "",

			# type: str
			"base_dir": "",

			# type: str
			"host": "",

			# type: str
			"port": "",

			# type: str
			"username": "",

			# type: str
			"password": "",
		},
	},
	# [END]
}
