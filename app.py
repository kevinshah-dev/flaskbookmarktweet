from flask import Flask, redirect, url_for, session, request, jsonify
import tweepy
import os
from flask_cors import CORS

consumer_token = "8nKoJIb7IC7mQRyJCqC5lPbj9"
consumer_secret = "7MMpibQpFbE11EklSPOCFdUtjsVEQClvil2JPC9RFaFwlvryJq"
callback_url = "https://bookmarktweet.vercel.app/twitter_callback"
client_id = os.environ.get("TWITTER_CLIENT_ID")
client_secret = os.environ.get("TWITTER_CLIENT_SECRET")



app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
CORS(app, resources={r"/*": {"origins": "*"}})

auth = tweepy.OAuth2UserHandler(
    client_id=client_id,
    redirect_uri=callback_url,
    scope=["tweet.read", "users.read", "bookmark.read", "follows.read", "like.read"],
    client_secret=client_secret
)




@app.route('/')
def index():
    print("Hello World")
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    session['email'] = data.get('email')
    print(f"Received email: {session['email']}")  # Logging to console
    try:
        redirect_url = auth.get_authorization_url()
        print(redirect_url);
        #session['request_token'] = auth.request_token
        print(f"Redirect URL: {redirect_url}")  # Logging to console
        return jsonify(redirect_url=redirect_url)
    except tweepy.TweepyException as e:
        print(f"Error: {e}")  # Logging error to console
        return jsonify(error='Failed to get request token'), 500

@app.route('/twitter_callback', methods=['GET', 'POST'])
def twitter_callback():
    state = session.get('state')
    #Print request
    data = request.get_json()
    session["authorization_url"] = data.get("authorization_url")
    print(f"request: {request}")
    authorization_response = request.url
    print(f"Authorization response: {authorization_response}")  # Logging to console

    try:
        token = auth.fetch_token(session["authorization_url"])
        print(f"Token: {token}")
        client = tweepy.Client(bearer_token=token['access_token'])
        print("Is this hitting?")
        print(client_id)
        print(client_secret)
        # Fetch bookmarks
        bookmarks = client.get_bookmarks(max_results=10)  # Adjust max_results as needed
        print(f"Bookmarks: {bookmarks.data}")  # Logging to console
        
        bookmark_urls = [f"https://twitter.com/{tweet['author_id']}/status/{tweet['id']}" for tweet in bookmarks.data]
        

        return jsonify(message=f"Successfully connected to Twitter! User's bookmarks have been sent to ")

    except Exception as e:
        print(f"Error: {e}")  # Logging error to console
        return jsonify(error='Failed to fetch access token'), 500




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))  # Use 8080 as default
    app.run(debug=True, host='0.0.0.0', port=port)
