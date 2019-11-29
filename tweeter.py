import tweepy, json, shutil, os
from time import sleep
from picamera import PiCamera

auth = tweepy.OAuthHandler("sJAvI2G4X9TQLMlGBTdh3RebH", "cu6amxA3vJ7OzsjwONTX4XfBZFGWYP8yfzCCbVn86MWj6Iq3uE")
auth.set_access_token("1047748675596931072-2ku6R9MkhoI5q4cDPTfNxwzGF2JsJd", "vTvurdFZqfyI2tTImRzIvSfjKhvunejsyATRM3w7ovhCe")
api = tweepy.API(auth)

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate

currentTime = ""
filename = ""
picFolder = "/home/pi/Documents/tweeter/pics/"
status = ["heyo", "lmao", "tets", "test"]

def sendTweet(a):
    global status
    randStatus = random.choice([0, len(status)]) + " @ " + str(a[:19])
    print(randStatus)
    api.update_with_media(filename, randStatus)

def deleteTweets():
    deletedTweets = 0
    timeline = tweepy.Cursor(api.user_timeline).items()
    for tweet in timeline:
        api.destroy_status(tweet.id)
        deletedTweets += 1
    print("Deleted " + str(deletedTweets) + " tweets")

def takePhoto(a):
    global filename
    filename = a + ".jpg".format(a)
    camera.start_preview(alpha=150)
    sleep(5)
    camera.capture(filename)
    camera.stop_preview()

def movePic(a, b):
    shutil.copy(a, b)
    print(a + " moved to " + b)

def delPic(a):
    os.remove(a)
    print("Deleted " + a)

for i in range(1, 2):
        localtime = time.asctime(time.localtime(time.time()))
        takePhoto(localtime)
        movePic(filename, picFolder)
        sendTweet(filename)
        # delPic(filename)
        sleep(10)
        # deleteTweets()
