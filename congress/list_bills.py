import json
import re

with open("mentions_of_bills.json") as f:
	data = json.load(f)

bills = set()

r = re.compile(r"(H\.R\. \d+|H\. Res\. \d+|S\. \d+|S\. Res\. \d+)")

for item in data:
	b = (re.search(r, item['transcript']).group(1))
	bills.add(b)

print("Number of bills:", len(bills))
print("Number of transcripts:", len(data))
print(f"Number of characters: {sum([len(item['transcript']) for item in data]):_}")
print(f"Number of words: {sum([len(item['transcript'].split()) for item in data]):_}")