import json
import logging
import os
import datetime
import random
from typing import Optional, Any

import scrapy


# we use multiple API keys to avoid hitting the rate limit
# we can use up to 1000 requests per hour per key
# rather than intelligently switching keys, we just randomly select one
# this should work out in the end

def get_api_key():
	api_keyset = os.environ["GOV_INFO_KEYSET"]
	keys = api_keyset.split(",")
	return random.choice(keys)


class GovInfoSpider(scrapy.Spider):
	name = "govinfo"

	def __init__(self, date=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if date is None:
			self.date = datetime.datetime.now()
			logging.info(f"No date supplied, setting date to {self.date}")
		else:
			self.date = datetime.datetime.fromisoformat(date)

	def start_requests(self):
		logging.debug("called start_requests of govinfo spider")
		url = f"https://api.govinfo.gov/packages/CREC-{self.date.date().isoformat()}/granules?" \
			  f"offset=0&pageSize=1000&api_key={get_api_key()}"
		yield scrapy.Request(url=url, callback=self.parse_datepage_list)

	def parse_datepage_list(self, response):
		logging.debug(f"called parse_datepage_list with {response.url}")
		resp = response.json()
		logging.debug(f"JSON Response: {resp}")
		if resp['nextPage'] is not None:
			yield scrapy.Request(url=resp['nextPage'], callback=self.parse_datepage_list)

		to_explore: list[tuple[str, str]] = [(item['granuleLink'], item['granuleClass'][0]) for item in resp['granules']
											 if
											 item['granuleClass'] in ("SENATE", "HOUSE")]

		for link in to_explore:
			yield scrapy.Request(url=link[0] + f"?api_key={get_api_key()}",
								 callback=self.parse_transcript_link_from_granule_link, meta={"body": link[1]})

	def parse_transcript_link_from_granule_link(self, response):
		r = response.json()
		try:
			yield scrapy.Request(url=r['download']['txtLink'] + "?api_key=" + get_api_key(),
								 callback=self.parse_transcript, meta=response.meta)
		except:
			logging.error(f"Error parsing {response.url} with body {response.meta['body']}")
			raise

	def parse_transcript(self, response):
		yield {
			"meta": response.meta,
			"transcript": response.text,
			"date": self.date.date().isoformat(),
		}


class DateRangeGovInfoSpider(GovInfoSpider):
	name = "daterangegovinfo"

	def __init__(self, start_date=None, end_date=None, backwards=False, *args, **kwargs):
		if start_date is None:
			self.start_date = datetime.datetime.now() - datetime.timedelta(days=30)
			logging.info(f"No date supplied, setting date to {self.start_date}")
		else:
			self.start_date = datetime.datetime.fromisoformat(start_date)

		if end_date is None:
			self.end_date = datetime.datetime.now()
			logging.info(f"No date supplied, setting date to {self.end_date}")
		else:
			self.end_date = datetime.datetime.fromisoformat(end_date)

		self.backwards = backwards

		# load state from previous run
		try:
			self.start_date = self.state["start_date"]
			self.end_date = self.state["end_date"]
			self.date = self.state["date"]
			self.backwards = self.state["backwards"]
		except KeyError:
			pass
		except AttributeError:
			pass

		try:
			# if we haven't set a date yet, set it
			if self.date is None:
				self.date = self.start_date if not self.backwards else self.end_date
		except AttributeError:
			self.date = self.start_date if not self.backwards else self.end_date

		# save state so we can persist
		self.state = {
			"start_date": self.start_date,
			"end_date": self.end_date,
			"date": self.date,
			"backwards": self.backwards,
		}

		logging.info(f"Starting date range spider with start date {self.start_date.date().isoformat()} " +
					 f"and end date {self.end_date.date().isoformat()}")
		logging.info(f"Active date is {self.date.date().isoformat()}")
		logging.info(f"Backwards is {self.backwards}")

		# init with date = self.date
		super().__init__(date=self.date.date().isoformat(), *args, **kwargs)

	def is_done(self):
		if self.backwards:
			return self.date < self.start_date
		else:
			return self.date > self.end_date

	def start_requests(self, **kwargs):
		# call the superclass method for each date in the range
		while not self.is_done():
			logging.debug(f"Starting requests for {self.date.date().isoformat()}")
			yield from super().start_requests()
			if self.backwards:
				self.date -= datetime.timedelta(days=1)
			else:
				self.date += datetime.timedelta(days=1)
			if self.date.weekday() == 0:
				logging.info(f"Finished requests for {self.date.date().isoformat()}")

			self.state["date"] = self.date
