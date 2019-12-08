import time, tweepy, json, shutil, os, random
from picamera import PiCamera

with open('twitterauth.json') as file:
    secrets = json.load(file)
auth = tweepy.OAuthHandler(secrets['consumer_key'], secrets['consumer_secret'])
auth.set_access_token(secrets['access_token'], secrets['access_token_secret'])
api = tweepy.API(auth)

camera = PiCamera(resolution=(1920, 1080), framerate=30)
camera.awb_mode = "fluorescent"

currentTime = ""
filename = ""
picFolder = "/home/pi/Documents/tweeter/pics/"
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
    randStatus = status[random.choice([0, len(status) - 1])] + " @ " + str(a[4:19])
    print(randStatus + " - " + c)
    api.update_with_media(c, randStatus)

def deleteTweets():
    deletedTweets = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        api.destroy_status(tweet.id)
        deletedTweets += 1
    print("Deleted " + str(deletedTweets) + " tweets")

def takePhoto(a):
    global filename
    a = a[4:16]
    a = a.replace(" ", "_")
    filename = a + ".jpg".format(a)
    camera.start_preview(alpha=150)
    time.sleep(5)
    camera.capture(filename)
    camera.stop_preview()

def movePic(a, b):
    shutil.copy(a, b)
    print(a + " moved to " + b)

def delPic(a):
    os.remove(a)
    print("Deleted " + a)

#while True:
for i in range(1, 2):
    localtime = time.asctime(time.localtime(time.time()))
    takePhoto(localtime)
    movePic(filename, picFolder)
    delPic(filename)
    sendTweet(filename, picFolder)
    time.sleep(10)
