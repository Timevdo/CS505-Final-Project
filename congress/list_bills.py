import json
import random
import re
import string

with open("mentions_of_bills.json") as f:
	data = json.load(f)

# shuffle the order of data
random.shuffle(data)

# fix whitespace in transcripts
# replace \n with newlines
for t in data:
	t['transcript'] = t['transcript'].replace("\\n", "\n")

# filter out transcripts that are less than 800 characters long (likely not a debate)

data = [t for t in data if len(t['transcript']) > 800]

# filter out transcripts that are less than 1500 characters long and contain the phrase
# "Congress has the power to enact this legislation pursuant to the following:"
# (ignore whitespace)

no_whitespace = {ord(c): None for c in string.whitespace}

data = [t for t in data if len(t['transcript']) > 1500 or
		"Congress has the power to enact this legislation pursuant to the following:".translate(no_whitespace)
		not in t['transcript'].translate(no_whitespace)]

bills = set()

r = re.compile(r"(H\.R\. \d+|H\. Res\. \d+|S\. \d+|S\. Res\. \d+)")

for item in data:
	b = (re.search(r, item['transcript']).group(1))
	bills.add(b)
	# print(item['transcript'])
	# input("Press enter for another transcript, or ctrl+c to exit")

print("Number of bills:", len(bills))
print("Number of transcripts:", len(data))
print(f"Number of characters: {sum([len(item['transcript']) for item in data]):_}")
print(f"Number of words: {sum([len(item['transcript'].split()) for item in data]):_}")
