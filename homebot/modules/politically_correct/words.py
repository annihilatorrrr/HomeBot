# Keep substrings last
WORDS = {
	"niggas": "respected sirs of dark skin pigmentation",
	"nigga": "respected sir of dark skin pigmentation",
	"niggers": "respected sirs of dark skin pigmentation",
	"nigger": "respected sir of dark skin pigmentation",
	"pajeets": "respectable indian sirs",
	"pajeet": "respectable indian sir",
}

def ireplace(old: str, new: str, text: str):
	"""https://stackoverflow.com/a/4773614."""
	idx = 0
	while idx < len(text):
		index_l = text.lower().find(old.lower(), idx)
		if index_l == -1:
			return text
		text = text[:index_l] + new + text[index_l + len(old):]
		idx = index_l + len(new)
	return text

def niceify(text: str):
	for bad_word, nice_word in WORDS.items():
		text = ireplace(bad_word, nice_word, text)
	return text
