from tweets import GETUserTweets

if __name__ == '__main__':
	# Add your auth tokens here
    consumer_key = ""
    consumer_secret = ""

    access_token = ""
    access_token_secret = ""

    if consumer_key == "" or consumer_secret == "" or access_token == "" or access_token_secret == "":
        print ("Please Provide Auth Tokens")
        input("Enter to EXIT.")

    screen_name = str(input("Twitter User Screen Name: @"))

    # Calling the GETUserTweet class from tweets file to access different functions
    api = GETUserTweets(screen_name, consumer_key, consumer_secret, access_token, access_token_secret)

    # Getting User Tweets
    api.GetTweets()

    # User's Friend & Followers List
    #Friends = api.FriendsList()
    #Followers = api.FollowersList()

    #for friend in Friends:
    #    print (friend, "\n")

    input("Enter to EXIT.")
