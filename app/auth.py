from flask import redirect
from flask_login import LoginManager
from app.models import User
from app.config import KEYROCK_ADMIN_PASSWORD, KEYROCK_ADMIN_USERNAME, KEYROCK_BASE_URL
from app.utils import get_x_auth_token
import requests

# Instantiate a LoginManager object
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
        This function loads a user by their ID.

        Args:
            user_id (str): The ID of the user to be loaded.

        Returns:
            User: The User object if the user is found.
            None: If the user is not found.
    """
    admin_token = get_x_auth_token(KEYROCK_ADMIN_USERNAME, KEYROCK_ADMIN_PASSWORD)
    headers = {'X-Auth-token': f'{admin_token}'}
    user_info_url = f"{KEYROCK_BASE_URL}/v1/users/{user_id}" 
    response = requests.get(user_info_url, headers=headers)
    if response.status_code in(200, 201):
        user_data = response.json()["user"]
        user = User(id=user_data["id"], username=user_data["username"], email=user_data["email"])
        return user
    else:
        print(f"Error fetching user data from Keyrock: {response.status_code} - {response.text}")
        return None
    
@login_manager.unauthorized_handler
def unauthorized():
    """
    This function handles unauthorized access by redirecting to the login page.

    Returns:
        A redirect response to the login page.
    """
    return redirect('login')