from flask import Flask, request, redirect, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

@app.route('/login')
def login():
    return redirect(f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=https://backend-developer-30333c40856e.herokuapp.com/')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_response = requests.post(
        'https://github.com/login/oauth/access_token',
        headers={'Accept': 'application/json'},
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        }
    )
    token_json = token_response.json()
    session['github_token'] = token_json['access_token']
    return redirect('/profile')

@app.route('/profile')
def profile():
    token = session.get('github_token')
    if not token:
        return redirect('/login')
    
    user_response = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': f'token {token}'}
    )
    user_json = user_response.json()
    return jsonify(user_json)

if __name__ == '__main__':
    app.run(debug=True)
