import json
import re

with open("./daterangegovinfo02.json") as f:
	data = json.load(f)

# check for any of the following:
# "H.R. \d"
# "H. Res. \d"
# "S. \d"
# "S. Res. \d"

r = re.compile(r"(H\.R\. \d|H\. Res\. \d|S\. \d|S\. Res\. \d)")

count = 0
chars = 0

items = []

for item in data:
	if r.search(item['transcript']):
		count += 1
		chars += len(item['transcript'])
		items.append(item)

with open("mentions_of_bills.json", "w") as f:
	json.dump(items, f)
