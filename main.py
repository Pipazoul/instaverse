import instaloader

# Load login and password from env file or from environment variables

import os
from dotenv import load_dotenv
import time
import random
import fastapi
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import base64
import xml.etree.ElementTree as ET
load_dotenv()

USER = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
print(USER)
print(PASSWORD)

apiUrl = os.getenv('APIURL')

# check if data folder exists
if not os.path.exists('data'):
    os.makedirs('data')
    

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


def activityPubUser(apiUrl, instaUser) :
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
            
        "@context": [
        "https://w3id.org/security/v1",
        "https://www.w3.org/ns/activitystreams",
            {
                "manuallyApprovesFollowers": "as:manuallyApprovesFollowers"
            }
        ],
        "id": "https://" + apiUrl + "/users/" + instaUser,
        "type": "Person",
        "following": "https://" + apiUrl + "/users/" + instaUser + "/following",
        "followers": "https://" + apiUrl + "/users/" + instaUser + "/followers",
        "inbox": "https://" + apiUrl + "/users/" + instaUser + "/inbox",
        "outbox": "https://" + apiUrl + "/users/" + instaUser + "/outbox",
        "preferredUsername": instaUser,
        "name": instaUser,
        "url": "https://" + apiUrl + "/" + instaUser,
        "manuallyApprovesFollowers": "false",
        "publicKey": {
            "id": "https://" + apiUrl + "/users/" + instaUser + "#main-key",
            "owner": "https://" + apiUrl + "/users/" + instaUser,
            "publicKeyPem":  "-----BEGIN PUBLIC KEY-----\n test \n-----END PUBLIC KEY-----",
        },
        "icon": {
            "type": "Image",
            "mediaType": "image/jpeg",
            "url": "https://" + apiUrl + "/data/" + instaUser + "/profile.jpg?v=1"
        },
        "endpoints": {
            "sharedInbox": "https://" + apiUrl + "/inbox"
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

@app.get("/users/{instaUser}/outbox")
def getUserOutboxRoute(instaUser: str, request: fastapi.Request):
    return {
    "@context": "https://www.w3.org/ns/activitystreams",
    "id": str(request.url),
    "type": "OrderedCollection",
    "totalItems": 0,
    "orderedItems": []
}

@app.get("/users/{instaUser}/following")
def getUserFollowingRoute(instaUser: str, request: fastapi.Request):
    return {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": str(request.url),
        "type": "OrderedCollection",
        "totalItems": 0,
        "orderedItems": []
    }

@app.get("/users/{instaUser}/followers")
def getUserFollowersRoute(instaUser: str, request: fastapi.Request):
    return {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": str(request.url),
        "type": "OrderedCollection",
        "totalItems": 0,
        "orderedItems": []
    }

# user/profile.jpg
@app.get("/{instaUser}/profile.jpg")
def getUserProfilePicRoute(instaUser: str, request: fastapi.Request):
    # open file and return it
    
    image = open('data/' + instaUser + '/profile.jpg', 'rb')
    
    print(image)

    # return base64.b64encode(image.read())
    encodedImage = base64.b64encode(image.read())
    return fastapi.Response(content=encodedImage, media_type="image/jpeg")

    

# create route .well-known/webfinger?resource=acct:{instaprofile}@{domain}
@app.get("/.well-known/webfinger")
def webfingerRoute(resource: str, request: fastapi.Request):
    
    
    
    # get url domain from fastapi 
    domain = request.headers['host']
    
    apiUrl = domain
    
    print(domain)
    
    # get insta profile from resource
    instaUser = resource.split('@')[0].split(':')[1]
    # get user info
    response = activityPubUser(apiUrl,instaUser)

    # format response
    response = {
    "subject": "acct:" + instaUser + "@" + apiUrl,
    "aliases": [
    "https://" + apiUrl + "/" + instaUser,
    "https://" + apiUrl + "/users/" + instaUser
    ],
    "links": [
        {
        "rel": "http://webfinger.net/rel/profile-page",
        "type": "text/html",
        "href":'https://' + apiUrl + "/" + instaUser
        },
        {
        "rel": "http://schemas.google.com/g/2010#updates-from",
        "type": "application/atom+xml",
        "href":'https://' + apiUrl + "/users/" + instaUser + ".atom"
        },
        {
        "rel": "self",
        "type": "application/activity+json",
        "href":'https://' + apiUrl + "/users/" + instaUser
        }
    ]
}

    return response


#  create route /users/{instaUser}.atom
@app.get("/users/{instaUser}.atom")
def userAtomRoute(instaUser: str, request: fastapi.Request):
    # return xml file
    
    return {
        "message": "ok"
    }


# create a route /user/{instaUser} 
@app.get("/users/{instaUser}")
def getUserInfoRoute(instaUser: str, request: fastapi.Request):
    
    #
    
    # get url domain from fastapi 
    domain = request.headers['host']
    
    print(instaUser)
    
    response = activityPubUser(domain,instaUser)
    return response
