#!/usr/src/Python-3.8.0 python3
import time, tweepy, json, shutil, os, random, urllib

with open('twitterauth.json') as file:
    secrets = json.load(file)
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth)

uploadError = True
localTime = ""
filename = ""
statusText = ""
picUrl = ""
picFolder = "/home/pi/Documents/tweeter/pics/"
urlArray = ["https://www.reddit.com/r/pics.json",
       "https://www.reddit.com/r/getmotivated.json",
       "https://www.reddit.com/r/roomporn.json",
       "https://www.reddit.com/r/earthporn.json",
       "https://www.reddit.com/r/astrophotography.json",
       "https://www.reddit.com/r/cozyplaces.json",
       "https://www.reddit.com/r/cityporn.json",
       "https://www.reddit.com/r/houseporn.json",
       "https://www.reddit.com/r/viewporn.json",
       "https://www.reddit.com/r/imaginaryinteriors.json",
       "https://www.reddit.com/r/architectureporn.json"]
statusArray = ["Look at this magnificent picture!",
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

def sendTweet(filename, picFolder, localTime, statusArray, statusText, picUrl):
    path = picFolder + filename
    statusText = random.choice(statusArray) + " @ " + str(localTime[:12]) + statusText
    print("Time: " + localTime + "\nPicture from: " + picUrl + "\nPicture saved in: " + path + "\nStatus: \'" + statusText + "\'")
    api.update_with_media(path, statusText)

def deleteTweets():
    deletedTweets = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        api.destroy_status(tweet.id)
        deletedTweets += 1
    print("Deleted " + str(deletedTweets) + " tweets")

def fetchPost(localTimeEdit, urlArray, picFolder):
    global filename
    global statusText
    global picUrl
    filename = localTimeEdit + ".jpg".format(localTimeEdit)
    chosenUrl = random.choice(urlArray)
    response = urllib.request.urlopen(urllib.request.Request(chosenUrl, headers={'User-Agent': 'tweeterReddit'}))
    data = json.loads(response.read())
    text = json.dumps(data)
    filePath = picFolder + filename
    urllib.request.urlretrieve(text[text.find('url": "https://i') + 7:text.find('"', text.find('url": "https://i') + 7)], filePath)
    picUrl = chosenUrl + "\n              "+ text[text.find('url": "https://i') + 7:text.find('"', text.find('url": "https://i') + 7)]
    statusText = " by u/" + text[text.find('author": "') + 10:text.find('"', text.find('author": "') + 10)]

#Countdown
for i in list(range(5))[::-1]:
    print(i + 1)
    time.sleep(1)

#for i in range(0, 24):
while True:
    localTime = time.asctime(time.localtime(time.time()))
    localTime = localTime[4:16]
    localTimeEdit = localTime.replace(" ", "_")
    localTimeEdit = localTimeEdit.replace(":", "_")
    fetchPost(localTimeEdit, urlArray, picFolder)
    while uploadError:
        try:
            sendTweet(filename, picFolder, localTime, statusArray, statusText, picUrl)
            uploadError = False
        except:
            uploadError = True
            print("FAILURE, probably the file size. Deleting " + picFolder + filename + ".\nTrying again...")
            os.remove(picFolder + filename)
            fetchPost(localTimeEdit, urlArray, picFolder)
    uploadError = True
    print("Success\n                                                                  ")
    time.sleep(3600)
