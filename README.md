# instaverse
instagram to fediverse

## Launch

`uvicorn main:app --reload`





## ActivityPub ressources




@yassinsiouda@fee2-5-51-141-112.eu.ngrok.io



fee2-5-51-141-112.eu.ngrok.io/.well-known/webfinger?resource=acct:yassinsiouda@fee2-5-51-141-112.eu.ngrok.io



# User request 
https://mastodon.doesnotexist.club/.well-known/webfinger?resource=acct:yassinsiouda@mastodon.doesnotexist.club

```json
{
"subject": "acct:yassinsiouda@mastodon.doesnotexist.club",
"aliases": [
"https://mastodon.doesnotexist.club/@yassinsiouda",
"https://mastodon.doesnotexist.club/users/yassinsiouda"
],
"links": [
{
"rel": "http://webfinger.net/rel/profile-page",
"type": "text/html",
"href": "https://mastodon.doesnotexist.club/@yassinsiouda"
},
{
"rel": "self",
"type": "application/activity+json",
"href": "https://mastodon.doesnotexist.club/users/yassinsiouda"
},
{
"rel": "http://ostatus.org/schema/1.0/subscribe",
"template": "https://mastodon.doesnotexist.club/authorize_interaction?uri={uri}"
}
]
}
```