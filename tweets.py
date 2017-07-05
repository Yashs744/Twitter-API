from OAuth import TwitterAPI
import twitter
import json
import datetime
import time
import csv
import os.path
import logging

class GETUserTweets:
	def __init__(self, screenName=None, consumer_key=None, consumer_secret=None, access_token=None, access_token_key=None):
		'''Constructor

			Parameter:
			screenName: The twitter name of the user whose followers you are fetching.
		        consumer_key (str): Your Twitter user's consumer_key.
		        consumer_secret (str): Your Twitter user's consumer_secret.
		        access_token (str): The oAuth access token value.
		        access_token_key (str): The oAuth access token's secret.
		'''

		# Initializing the Logger
		self.logger = logging.getLogger(__name__)
		logging.basicConfig(filename = "LOGS.log", level = logging.DEBUG, 
							format = "%(asctime)s:%(levelname)s - %(lineno)d:%(message)s")

		# Calling the Twitter API
		try:
			self.api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_key).API()
		except twitter.error.TwitterError as error:
			self.logger.error(str(error))
			exit(1)

		self.screen_Name = screenName

	def _UnicodeDecode(self, text):
		'''
			Function to decode tweet text

			Parameter:
				text: Tweet text to be decoded

			Returns:
				Decoded text 
		'''
		try:
			return text.encode('utf-8').decode()
		except UnicodeDecodeError:
			return text.encode('utf-8')

	def _ProcessTweets(self, tweet):
		'''
			Function to Process the Status.

			Parameter:
				tweet: Tweet of the User.

			Returns:
				Tweet ID, Text, User Name, Number of Likes, Retweet Count, Time
		'''
		Tweet_ID = str(tweet.id)
		Screen_Name = tweet.user.screen_name
		Tweet_Text = '' if not tweet.text else self._UnicodeDecode(tweet.text)
		Likes = tweet.favorite_count
		Retweet = tweet.retweet_count
		Tweet_Time = datetime.datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
		Tweet_Time = Tweet_Time.strftime('%Y-%m-%d %H:%M:%S')

		return [Tweet_ID, Screen_Name, Tweet_Text, Likes, Retweet, Tweet_Time]

	def write_toCSV(self, Tweets):
		'''
			Function to Write Tweets to a CSV file with the same name as of the user.

			Parameters:
				Tweets: List of Tweets

			Returns:
				Creates a new CSV file and returns control to the calling function
		'''
		path = "CSV Files/"
		if not os.path.exists(path):
                        os.makedirs(path)

		filename = str(self.screen_Name + ".csv")

		with open(os.path.join(path, filename), 'w', encoding="utf-8", newline='') as file:
			w = csv.writer(file)
			w.writerow(['Tweet ID', 'Screen Name', 'Text', 'Likes', 'Retweet Count', 'Tweet Date-Time'])

			for tweet in Tweets:
				tweet_data = self._ProcessTweets(tweet)
				w.writerow(tweet_data)

			file.close()

	def FollowersList(self, ScreenName = None):
		'''
			Function to get the List of Followers using the ScreenName and Number of followers.

			Parameters:
				ScreenName: The twitter name of the user whose followers you are fetching.
							Default is None i.e if not passed anything will take for the root user.

			Return:
				A List of Followers. 
		'''
		Followers = []

		if ScreenName is None:
			ScreenName = self.screen_Name

		try:
			followers = self.api.GetUser(screen_name = ScreenName).followers_count
		except twitter.error.TwitterError as error:
			self.logger.error(str(error))

		for user in self.api.GetFollowers(screen_name = ScreenName, total_count = followers):
			Followers.append(user.screen_name)

		return Followers

	def FriendsList(self, ScreenName = None):
		'''
			Function to get the Followers using the ScreenName and Number of followers.

			Parameters:
				ScreenName: The twitter name of the user whose followers you are fetching.
							Default is None i.e if not passed anything will take for the root user.

			Return:
				A List of Friends. 
		'''
		Friends = []

		if ScreenName is None:
			ScreenName = self.screen_Name

		try:
			friends = self.api.GetUser(screen_name = ScreenName).friends_count
		except twitter.error.TwitterError as error:
			self.logger.error(str(error))

		for user in self.api.GetFriends(screen_name = ScreenName, total_count = friends):
			Friends.append(user.screen_name)

		return Friends

	def GetTweets(self, ScreenName = None):
		'''
			Function to fetch Status from the User Timeline using the ScreenName.

			Parameters:
				ScreenName: The twitter name of the user whose followers you are fetching.
							Default is None i.e if not passed anything will take for the root user.

			Returns:
				Return back the control to the calling function if a error occurs otherwise calls
				_ProcessStatus() function and passes the UserTimeline
		'''
		UserTimeline = []

		if ScreenName is None:
			ScreenName = self.screen_Name

		try:
			latestTweets = self.api.GetUserTimeline(screen_name = ScreenName, count=200)
			UserTimeline.extend(latestTweets)
			
			oldTweets = UserTimeline[-1].id - 1
			
			while len(latestTweets) > 0:
				print ("Getting Tweets Before Tweet ID {}".format(oldTweets))
	
				latestTweets = self.api.GetUserTimeline(screen_name = ScreenName, count=200, max_id=oldTweets)
				UserTimeline.extend(latestTweets)
				
				oldTweets = UserTimeline[-1].id - 1
				
				print ("{} Tweets Downloaded".format(len(UserTimeline)))

		except twitter.error.TwitterError as error:
			self.logger.error(str(error))
			return -1

		self.write_toCSV(UserTimeline)

if __name__ == '__main__':
        print ("Error: cannot run file directly")
        self.logger.error("cannot run GETUserTweets class directly")
        exit(1)
