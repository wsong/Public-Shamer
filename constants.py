FB_APP_ID = ""
FB_REDIRECT_URI = ""
FB_APP_SECRET = ""

FB_OAUTH_DIALOG_URL = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode({"client_id": APP_ID, "redirect_uri": REDIRECT_URI, "scope": "publish_stream,offline_access"})
FB_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"
FB_CURRENT_USER_URL = "https://graph.facebook.com/me?"
FB_FEED_URL = "https://graph.facebook.com/feed"

LASTFM_API_KEY = ""
