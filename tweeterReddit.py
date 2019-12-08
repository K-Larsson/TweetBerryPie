#!/usr/src/Python-3.8.0 python3
import time, tweepy, json, shutil, os, random, urllib

with open('twitterauth.json') as file:
    secrets = json.load(file)
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth)

picPath = "C:/users/megak/desktop/"
picFolder = "/home/pi/Documents/tweeter/pics/"
url = "https://www.reddit.com/r/pics.json"
filename = ""
status = ["Look at this magnificent tree!",
          "Do you even beep boop, bro?",
          "Another day, another picture!",
          "I love the smell of pictures in the morning... Or whatever time it is.",
          "Frankly my dear, I dont give a circuit.",
          "I'm going to make him a picture he can't refuse.",
          "Go ahead, make my picture.",
          "May the picture be with you.",
          "You talking to m... I mean, uh, beep boop!",
          "TweetBerry, TweetBerry Pie",
          "Show me the picture!",
          "Hey! I'm working here!",
          "You can't handle the picture!",
          "You're gonna need a bigger picture.",
          "I'll be back.",
          "Mama always said life is like a box of pictures.",
          "Houston, we have a picture.",
          "Do I feel picturesque? Well, do ya, punk?"]

def sendTweet(a, b):
    global status
    c = b + a
    randStatus = random.choice(status) + " @ " + str(a[:12])
    print(randStatus + " - " + c)
    api.update_with_media(c, randStatus)

def deleteTweets():
    deletedTweets = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        api.destroy_status(tweet.id)
        deletedTweets += 1
    print("Deleted " + str(deletedTweets) + " tweets")

def fetchPost(localTime, url, path):
    global filename
    localTime = localTime[4:16]
    localTime = localTime.replace(" ", "_")
    localTime = localTime.replace(":", "_")
    filename = localTime + ".jpg".format(localTime)
    response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'tweeterReddit'}))
    data = json.loads(response.read())
    text = json.dumps(data)
    path = path + filename
    urllib.request.urlretrieve(text[text.find('url": "https://i') + 7:text.find('"', text.find('url": "https://i') + 7)], path)
    picUrl = text[text.find('url": "https://i') + 7:text.find('"', text.find('url": "https://i') + 7)]
    statusText = "Owner of the picture: " + text[text.find('author": "') + 10:text.find('"', text.find('author": "') + 10)]
    print("Time: " + localTime + "\nStatus: \'" + statusText + "\'\nPicture from: " + picUrl + "\nPicture saved in: " + path)

#Countdown
for i in list(range(5))[::-1]:
    print(i + 1)
    time.sleep(1)

#while True:
for i in range(0, 24):
    localtime = time.asctime(time.localtime(time.time()))
    fetchPost(localtime, url, picFolder)
    sendTweet(filename, picFolder)
    time.sleep(3600)
