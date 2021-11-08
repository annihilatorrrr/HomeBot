config = {
	# [START]
	"bot": {
		# Add here your HTTP API bot token, get it from @BotFather
		# type: str
		"api_token": "",
	},

	# Module - Bridgey
	"bridgey": {
		# Enable the module
		# type: bool
		"enable": False,

		# Discord bridge
		"discord": {
			# Enable the bridge
			# type: bool
			"enable": False,

			# ID of the channel to bridge
			# type: int
			"channel_id": None,

			# Bot token
			# type: str
			"token": "",

			# Channel webhook URL
			# type: str
			"webhook_url": "",
		},

		"telegram": {
			# Enable the bridge
			# type: bool
			"enable": False,

			# ID or username of the chat to bridge
			# type: int | str
			"chat_id": "",
		},
	},

	# Module - CI
	# Read this before continuing: https://github.com/SebaUbuntu/HomeBot/wiki/Module-%7C-CI#variables
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

		# type: list[str]
		"devices": [],

		# type: str
		"chat_id": "",

		# type: str
		"photo_url_base": "",

		# type: str
		"donation_link": "",
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
