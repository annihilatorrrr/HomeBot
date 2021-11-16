from requests import post

URL = "https://nekobin.com"

def to_nekobin(data: str) -> str:
	"""Upload a string to Nekobin and return its URL."""
	resp = post(f"{URL}/api/documents", json={"content": data}).json()
	key = resp.get("result").get("key")
	return f"{URL}/{key}"
