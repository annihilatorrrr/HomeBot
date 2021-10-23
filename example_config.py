config = {
	# [START]
	"bot": {
		# Add here your HTTP API bot token, get it from @BotFather
		# type: str
		"api_token": "",
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
