import instaloader

# Load login and password from env file or from environment variables

import os
from dotenv import load_dotenv
import time
import random
import fastapi
from fastapi.staticfiles import StaticFiles
load_dotenv()

USER = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
print(USER)
print(PASSWORD)

apiUrl = os.getenv('APIURL')



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
    insta = instaloader.Instaloader(dirname_pattern='data/{target}/')

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

    # save profile info + user profile pic to name profile.jpg
    print('saving profile info')

    # create folder for user
    if not os.path.exists('data/' + instaUser):
        os.makedirs('data/' + instaUser)    
    
    insta.context.get_and_write_raw(profile.profile_pic_url, 'data/' + instaUser + '/profile.jpg')
    
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
    

    # get user info
    # check if user exists in folder
    # if not get user info
    # if yes get user info from folder
    
    if os.path.exists('data/' + instaUser):
        # get profile bio
        print('getting profile bio')
        with open('data/' + instaUser + '/bio.txt', 'r') as f:
            summary = f.read()
        # return url to profile pic path to 

    else:
        # get user info
        getUserInfo(instaUser)
        # get profile bio
        print('getting profile bio')
        with open('data/' + instaUser + '/bio.txt', 'r') as f:
            summary = f.read()


    return {
        "name": name,
        "type": type,
        "summary": summary,
        "preferredUsername": preferredUsername,
        "id": id,
        "icon": {
        "type": "Image",
        "mediaType": "image/jpeg",
        "url": apiUrl+'/data/' + instaUser + '/profile.jpg'
    },
    }


#getUserInfo('instagram')
# create a route /getPosts/{instaUser}
app = fastapi.FastAPI()
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.get("/getPosts/{instaUser}")
def getPostsRoute(instaUser: str):
    #getPosts(instaUser)


    return {"message": "ok"}

# create a route /user/{instaUser}
@app.get("/user/{instaUser}")
def getUserInfoRoute(instaUser: str):
    response = activityPubUser(instaUser)
    return response



# create route .well-known/webfinger?resource=acct:{instaprofile}@{domain}
@app.get("/.well-known/webfinger")
def webfingerRoute(resource: str):
    # get insta profile from resource
    instaUser = resource.split('@')[0].split(':')[1]
    # get user info
    response = activityPubUser(instaUser)

    # format response
    response = {
    "subject": "acct:" + instaUser + "@" + apiUrl,
    "aliases": [
    "https://mastodon.doesnotexist.club/@yassinsiouda",
    "https://mastodon.doesnotexist.club/users/yassinsiouda"
    ],
    "links": [
        {
        "rel": "http://webfinger.net/rel/profile-page",
        "type": "text/html",
        "href": apiUrl + "/@" + instaUser
        },
        {
        "rel": "self",
        "type": "application/activity+json",
        "href": apiUrl + "/users/" + instaUser
        },
        {
        "rel": "http://ostatus.org/schema/1.0/subscribe",
        "template": apiUrl + "/authorize_interaction?uri={uri}"
        }
    ]
}

    return response
