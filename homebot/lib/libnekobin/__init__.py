from requests import post

URL = "https://nekobin.com"

def to_nekobin(data: str) -> str:
	"""Upload a string to Nekobin and return its URL."""
	data = {"content": data}

	resp = post(f"{URL}/api/documents", json=data)
	resp.raise_for_status()
	resp_json = resp.json()

	key = resp_json.get("result").get("key")
	return f"{URL}/{key}"
