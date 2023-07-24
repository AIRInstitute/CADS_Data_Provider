
from flask import current_app, make_response, redirect, request, jsonify, Blueprint, render_template, url_for, session
from app.auth import load_user
from flask_login import current_user, login_required, login_user, logout_user
from app.config import KEYROCK_ACCES_TOKEN_URL, KEYROCK_AUTHORIZATION_URL, APP_CLIENT_ID, APP_CLIENT_SECRET, DEVELOPMENT,KEYROCK_BASE_URL,  APP_REDIRECT_URI, KEYROCK_LOGOUT, KEYROCK_USER_INFO_URL
import requests
import secrets
from flask.sessions import SecureCookieSessionInterface



main_blueprint = Blueprint("routes", __name__)


if DEVELOPMENT:
    @main_blueprint.route("/")
    @login_required
    def index():
        # Route for the home page which requires login, displays user information.
        user = current_user
        return render_template("index.html", user=user)
    

    @main_blueprint.route("/entity/<entity_type>", methods=["GET"])
    @login_required
    def entity_type(entity_type):
        # Route for displaying specific entity type, requires login, displays user and entity type information.
        user = current_user
        return render_template("entity_type.html", user=user, entity_type=entity_type)


    @main_blueprint.route("/tokens", methods=["GET"])
    def get_tokens():
        # Route for displaying tokens, requires login, displays user information.
        user = current_user
        return render_template("tokens.html", user=user)



    @main_blueprint.route("/register", methods=["GET"])
    def register():
        # Route for registration page, checks if user is already logged in, otherwise displays registration form.
        if current_user.is_authenticated:
            return jsonify({"error": "You are already logged in."}), 403
        return render_template("register.html")
        
        

    @main_blueprint.route("/login", methods=["GET"])
    def login():
        # Route for login page, checks if user is already logged in, otherwise redirects to Keyrock authentication.
        if current_user.is_authenticated:
            return jsonify({"error": "You are already logged in."}), 403
        
        state = secrets.token_hex(16)
        session['state'] = state

        app_instance = current_app._get_current_object()

        secure_cookie = SecureCookieSessionInterface().get_signing_serializer(app_instance)

        keyrock_auth_url = f'{KEYROCK_AUTHORIZATION_URL}?response_type=code&client_id={APP_CLIENT_ID}&redirect_uri={APP_REDIRECT_URI}&state={state}'

        secure_cookie_cookie = secure_cookie.dumps({"state": state})
        response = make_response(redirect(keyrock_auth_url))
        response.set_cookie("state_cookie", secure_cookie_cookie)
        return response
    

   
    @main_blueprint.route("/callback")
    def callback():
        # Callback route for Keyrock to redirect after successful login, exchanges code for access token, and logs the user in.
        code = request.args.get('code')

        app_instance = current_app._get_current_object()
        secure_cookie = SecureCookieSessionInterface().get_signing_serializer(app_instance)
        state_cookie = request.cookies.get("state_cookie")
        stored_state = None
        if state_cookie:
            stored_state = secure_cookie.loads(state_cookie).get("state")


        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': APP_CLIENT_ID,
            'client_secret': APP_CLIENT_SECRET,
            'redirect_uri': APP_REDIRECT_URI,
        }
        response = requests.post(KEYROCK_ACCES_TOKEN_URL, data=payload)

        token_data = response.json()
        access_token = token_data.get('access_token')
        session['access_token'] = access_token

        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(KEYROCK_USER_INFO_URL, headers=headers)
        user_data = user_response.json()
        session['user_data'] = user_data
        user_id = user_data.get('id')
        user = load_user(user_id)
        
        if user:
            login_user(user)  
            return redirect(url_for('routes.index'))
        else:
            return redirect(url_for('routes.login', error="User not found or could not be logged in."))



    @main_blueprint.route('/welcome', methods=["GET"])
    def welcome():
        # Route for welcome message, displays the username of the logged in user.
        user_data = session.get('user_data', {})
        return f'Welcome {user_data.get("username")}!'


    @main_blueprint.route("/logout", methods=['POST'])
    def logout():
        # Route for logout, logs out the user, clears the session, and redirects to Keyrock logout page.
        logout_user()  
        session.clear()  
        keyrock_logout_url = f'{KEYROCK_LOGOUT}'
        return redirect(url_for('routes.index'))

    

    @main_blueprint.route("/user/app/<app_id>", methods=["GET"])
    def user_from_app_view(app_id):
        # Route for displaying user information based on the provided app ID.
        user = current_user
        return render_template("user_from_app.html", user=user, app_id=app_id)
    

 