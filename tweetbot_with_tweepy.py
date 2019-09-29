import tweepy

#Authenticate to Twitter
auth = tweepy.OAuthHandler("Insert_your_info")

auth.set_access_token(
    'Insert_your_info')

#Create API object
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

try:
    api.verify_credentials()
    print("Authorization OK")
except:
    print("Error during authentication")


#Methods for User Timelines
#This code snippet prints the author and text of the last tweets in your home timeline:

timeline = api.home_timeline()
for tweet in timeline:
    print(f"{tweet.user.name} said  {tweet.text}")

#Methods for Tweets

#These methods have to do with creating, fetching, and retweeting tweets.
#The following code uses Tweepy to create a tweet with some text:

#api.update_status("BLLame it on the a-a-a-a-cting")

#Methods for Users
#Methods in this group enable you to search users with a filter criteria, fetch user details, and #list the followers of any user, as long as that user account is public.

user = api.get_user("justanesta")

print("User details:")
print(user.name)
print(user.description)
print(user.location)

print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)

#get_user() returns an object containing the user details. This returned object also has methods to access information related to the user. You used the followers attribute to get the list of followers.

#Methods for followers

#This group of methods deals with following and unfollowing users, querying a user’s followers, and listing the accounts any user is following.

#This code shows how you can use Tweepy to start following @realpython:

api.create_friendship("realpython")
#create_friendship() adds @realpython to the list of accounts that you follow.

#Methods for Your Account

#These methods allow you to read and write your own profile details.
#For example, you can use this code snippet to update your profile description:

api.update_profile(description="Sitting at the intersection between John Mulaney and Larry David")

#Methods for Likes

#Using these API methods, you can mark any tweet as Liked or remove the Like mark if it was already added.

#You can mark the most recent tweet in your home timeline as Liked as follows:

tweets = api.home_timeline(count=1)
tweet = tweets[0]
print(f"Liking tweet {tweet.id} of {tweet.author.name}")
api.create_favorite(tweet.id)

#Methods for Blocking Users

#This group of methods deals with blocking and unblocking users, as well as listing blocked users.

#Here’s how you can see the users that you have blocked:

for block in api.blocks():
    print(block.name)

#Methods for Searches
