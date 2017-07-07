# Twitter-API
Using Python-Twitter Library and Twitter API to access twitter and gather data from different users.

OAuth.py - It contains the class TwitterAPI which call the Twitter API and returns api object.
           We pass 4 keys (consumer key, consumer secret, access token, access token secret) to the twitter.Api() function
           along with sleep_on_limit_rate=True which tells the api to sleep when we reach our api call limit.
           It returns the api object to the calling class.
           
tweets.py - GETUserTweets class is the main class which handles all the backend work of fetching the UserTimeline, Friends List
            Followers List and then pre-processing it in a human reable form using JSON library and Python inbuilt Lists.
            It also contains a function to save the data in a CSV formatted file for further analysis.
            
main.py - Copy and Paste your key here and sit back and relax. It'll handle all the work.
          It basically calls the GETUserTweeets class from tweets.py file and performs the magic.
          You can make changes in here like what function to call from GETUserTweets etc.
          
GETUserTweets class only contains three method GetUserTimeline, GetFriendsList and GetFollowersList but you can add more functions as per your need

GetTweets function inside GETUserTweets class fetches all tweets from the timeline of the user. Twitter have a limit to it's API calls so
we cannot get all data in a single call to resolve this problem I'm making multiple calls but even after this we can only get 3200 tweets.
