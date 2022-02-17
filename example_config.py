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
		},

		"matrix": {
			# Enable the bridge
			# type: bool
			"enable": False,

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
			# Enable the bridge
			# type: bool
			"enable": False,

			# ID or username of the chat to bridge
			# type: int | str
			"chat_id": "",
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

	# Module - Politically correct
	"politically_correct": {
		# type: bool
		# Enable the module
		"enable": False,

		# type: list[str]
		# Chats where the module will be enabled
		"chat_ids": [],
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
