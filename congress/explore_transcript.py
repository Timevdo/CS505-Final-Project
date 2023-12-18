# display a random transcript entry from daterangegovinfo02.json

import json
import random
import string

with open("./daterangegovinfo02.json") as f:
	data = json.load(f)

while True:
	print("\n" * 100)
	item = random.choice(data)

	# replace \n with newlines
	transcript = item['transcript'].replace("\\n", "\n")
	transcript = transcript.translate({ord(c): None for c in string.whitespace if c != ' '})
	transcript = " ".join(transcript.split())
	print(transcript)
	input("Press enter for another transcript, or ctrl+c to exit")


