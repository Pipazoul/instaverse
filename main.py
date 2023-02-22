import instaloader

# Load login and password from env file or from environment variables

import os
from dotenv import load_dotenv
import time
import random
import fastapi
load_dotenv()

USER = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
print(USER)
print(PASSWORD)



def getPosts(instaUser):
    # Get instance dirname posts/instaUser
    insta = instaloader.Instaloader(dirname_pattern='data/{target}/posts')


    # try to load session usin instaloader
    try:
        insta.load_session_from_file(USER)
    except:
        # login
        insta.login(USER, PASSWORD)

        # save session
        insta.save_session_to_file()


    # sleep random time between 1 and 5 seconds
    print('sleeping')
    time.sleep(random.randint(1, 5))

    # Get a user profile from an instance
    print('getting profile')
    profile = instaloader.Profile.from_username(insta.context, instaUser)

    # sleep random time between 1 and 5 seconds
    print('sleeping')
    time.sleep(random.randint(1, 5))

    # Get all posts from the past 24 hours
    print('getting posts')
    posts = profile.get_posts()

    # sleep random time between 1 and 5 seconds
    print('sleeping')
    time.sleep(random.randint(1, 5))

    # download last 2 posts
    print('downloading posts')
    i = 0
    for post in posts:
        if i <= 2:
            insta.download_post(post, target=instaUser) 
            i =  i+1
            print('i' + str(i))
            print('sleeping')
            time.sleep(random.randint(1, 5))
        else:
            break


def getUserInfo(instaUser) :
    # Get instance
    insta = instaloader.Instaloader(dirname_pattern='data/{target}/posts')

    # try to load session usin instaloader
    try:
        insta.load_session_from_file(USER)
    except:
        # login
        insta.login(USER, PASSWORD)

        # save session
        insta.save_session_to_file()

    # sleep random time between 1 and 5 seconds
    print('sleeping')
    time.sleep(random.randint(1, 5))

    # Get a user profile from an instance
    print('getting profile')
    profile = instaloader.Profile.from_username(insta.context, instaUser)

    # save profile info + user profile pic
    print('saving profile info')
    insta.download_profile(profile, profile_pic_only=True)
    # get profile bio 
    print('getting profile bio')
    profileBio = profile.biography
    # save profile bio
    print('saving profile bio')
    with open('data/' + instaUser + '/bio.txt', 'w') as f:
        f.write(profileBio)


def activityPubUser(instaUser) :
    name = instaUser
    type = 'Person'
    summary = 'Empty'
    preferredUsername= instaUser
    id = 'https://www.instagram.com/' + instaUser
    

#getUserInfo('instagram')
# create a route /getPosts/{instaUser}
app = fastapi.FastAPI()

@app.get("/getPosts/{instaUser}")
def getPostsRoute(instaUser: str):
    #getPosts(instaUser)


    return {"message": "ok"}