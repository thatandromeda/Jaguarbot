import sys
import tweepy
import MySQLdb

from datetime import datetime, timedelta
from mysettings import *
from time import sleep

# to avoid irritating launchd; not needed if you're running from cron
sleep(15)

# authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# get today's date and the date six months (180 days) from now
today = datetime.now()
sixmonths = timedelta(180)
later = today + sixmonths

# convert these dates to SQL-friendly yyyy-mm-dd format
# and give them tweet-friendly labels for use later
today = [str(today)[:10], "TODAY: "]
later = [str(later)[:10], "In 6 months: "]
dates = [today, later]

# open db connection
conn = MySQLdb.connect (host = SQL_HOST,
						user = SQL_USER,
						passwd = SQL_PASSWORD,
						db = SQL_DB)
cursor = conn.cursor()

# get ids of any nodes for our dates and examine each for info
for date in dates:
	cursor.execute("SELECT nid FROM content_field_startdaterepeat WHERE field_startdaterepeat_value LIKE '%"+date[0]+"%'")

	while(1):
		row = cursor.fetchone()
		if row == None:
			break
		node_id = str(row[0]) # fetchone returns tuples; we just want the string
	
		# find this node's URL (link to external resources for event)
		url = conn.cursor()
		url.execute("SELECT field_urlstypelink_url FROM content_type_jaguar_two WHERE nid="+node_id)
		node_url=url.fetchone()[0]
		url.close()
	
		# find this node's title, so we have something human-friendly to tweet
		title = conn.cursor()
		title.execute("SELECT title FROM `node` WHERE nid ="+node_id)
		node_title=title.fetchone()[0]
		title.close()
		
		# make sure the tweet length doesn't exceed 140; if too long, truncate
		# leave 13 for date label, 20 for URL wrapping (t.co max as of Dec 2011)
		# if we were good people we'd issue a request to Twitter to find out the current t.co maximum length
		# but we're not
		# yet
		if len(node_title) > 107:
			node_title = node_title[:104]+"..."

		# construct tweet -- if no URL for node, send them to Team J's project page for more info instead
		if url != None:
			tweet = date[1]+node_title+" ("+node_url+")"
		else:
			tweet = date[1]+node_title+" (http://jaguars.andromedayelton.com)"
		
		# actually tweet it! the part humans see
		api.update_status(tweet)
		
		# in case there are lots of status updates today, we should sleep between them so twitter doesn't think we're a robot
		# well
		# so twitter doesn't think we're a bad robot
		sleep(1)

# make sure to clean up your toys and put them away
cursor.close()
conn.close()
  
# TODO
## figure out how to handle it when multiple objects get returned by the first select
## decide how to handle long-duration events
## deal with unicode characters (e.g. in El dia)
## issue t.co max length request and update truncation code accordingly
## does it matter that I'm only fetching the first thing returned for my second 2 SQL queries?
## filter ALDirect out of six-months-in-advance warnings; consider how to use tags or other data to give more intelligent advance warnings
## find out how frequently I can hit Twitter before it decides I'm evil and test for high-update times/update sleep() accordingly