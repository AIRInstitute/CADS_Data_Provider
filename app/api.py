
from flask import Blueprint, request, jsonify
from app.models import  User
from app.utils import add_policy, api_key_required, get_token, get_token_with_jwt, get_x_auth_token, list_policies, store_policy_in_ar, test_policy
from flask_login import current_user, login_required
from app.config import  DEVELOPMENT, APP_KEYROCK_PASSWORD, APP_KEYROCK_USERNAME, KEYROCK_APPLICATION_URL_1, KEYROCK_APPLICATION_URL_2, KONG_ENTITIES, KONG_ENTITIES_TYPE, KEYROCK_USERS_URL
import requests
from flask_restx import  Resource, Namespace
from app.models import db

# Defining Blueprint for the API
api_blueprint = Blueprint("api", __name__)


# Namespaces for different operations
authentication_ns = Namespace('authentication', description='Authentication Operations')
authorization_ns = Namespace('authorization', description='Authorization Operations')
context_broker_ns = Namespace('context-broker', description='Context Broker Operations')
keyrock_ns = Namespace('keyrock', description='Keyrock Operations')

def get_namespaces():
    # Function to return all namespaces
    return [authentication_ns, authorization_ns, context_broker_ns, keyrock_ns]

def conditional_decorator(decorator1, decorator2):
    # Conditional decorator function, returns different decorator based on the environment
    def wrapper(func):
        if DEVELOPMENT:
            return decorator1(func)
        else:
            return decorator2(func)
    return wrapper


@authentication_ns.route("/get_access_token")
class GetAccessToken(Resource):
    # Resource class for getting access token
    @authentication_ns.doc('get_access_token')
    @authentication_ns.doc(params={'email': {'description': 'User email', 'required': True},
                                  'password': {'description': 'User password', 'required': True}})
    def get(self):
        username = request.args.get('email')
        password = request.args.get('password')
        return get_token(username=username, password=password)


@authentication_ns.route("/get_x_access_token")
class GetXAccessToken(Resource):
    # Resource class for getting extended access token
    @authentication_ns.doc('get_x_access_token')
    @authentication_ns.doc(params={'email': {'description': 'User email', 'required': True},
                                  'password': {'description': 'User password', 'required': True}})
    def get(self):
        username = request.args.get('email')
        password = request.args.get('password')
        return get_x_auth_token(username=username, password=password)


@authentication_ns.route('/get_jwt_access_token')
class GetJWTAccessToken(Resource):
    # Resource class for getting access token using JWT
    @authentication_ns.doc('get_jwt_access_token')
    def get(self):
        return get_token_with_jwt()


@context_broker_ns.route("/entity/<entity>")
class GetEntitiesByType(Resource):
    # Resource class for fetching entities by their type
    @context_broker_ns.doc('get_entities_by_type')
    @context_broker_ns.param('entity', 'The type of entity')
    @conditional_decorator(login_required, api_key_required)
    def get(self, entity):
        token = get_token_with_jwt()
        headers = {
            "Authorization" : f'Bearer {token}',
            "Content-Type" :  "application/json"
        }

        url = f"{KONG_ENTITIES_TYPE}{entity}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            entities = response.json()
            return {"entities": entities}, 200
        else:
            return {"error": f"Error al obtener entidades del Context Broker: {response.status_code} - {response.text}"}, response.status_code



@context_broker_ns.route("/entity/id/<entity_id>")
class GetEntityById(Resource):
    # Resource class for fetching an entity by its ID
    @context_broker_ns.doc('get_entity_by_id')
    @context_broker_ns.param('entity_id', 'The ID of the entity to fetch')
    @conditional_decorator(login_required, api_key_required)
    def get(self, entity_id):
        token = get_token_with_jwt()
        headers = {
            "Authorization" : f'Bearer {token}',
            "Content-Type" :  "application/json"
        }

        url = f"{KONG_ENTITIES}/{entity_id}"

        response = requests.get(url, headers=headers)
        

        if response.status_code == 200:
            entity = response.json()
            return {"entity": entity}, 200
        else:
            return {"error": f"Error al obtener entidad del Context Broker: {response.status_code} - {response.text}"}, response.status_code


@context_broker_ns.route("/entity/types")
class GetAllEntityTypes(Resource):
    # Resource class for fetching all entity types
    @context_broker_ns.doc('get_all_entity_types')
    @conditional_decorator(login_required, api_key_required)
    def get(self):
        return {
            "entity_types" : [
                "AgriFarm", "AgriCarbonFootprint", "AgriCrop", "AgriGreenHouse", "AgriParcel", "AgriParcelOperation", "AgriParcelRecord", "AgriSoil", "AgriSoilState", "AgriYield"
            ]
        }




@authorization_ns.route("/store-policy")
class StoreUserPolicy(Resource):
    # Resource class for storing user policy
    @authorization_ns.doc('store_user_policy')
    @authorization_ns.param('entity_type', 'Entity type', required=True)
    @authorization_ns.param('action', 'Action', required=True)
    @authorization_ns.param('allowed_attributes', 'Allowed attributes', required=True)
    @api_key_required
    def post(self):
        entity_type = request.args.get("entity_type")
        action =  request.args.get("action")
        allowed_attributes = request.args.get("allowed_attributes")
        if not (entity_type and action and allowed_attributes):
            return {"error": "Faltan campos obligatorios."}, 400

        policy = add_policy(entity_type, action, allowed_attributes)
        message, error = store_policy_in_ar(policy)

        return message, error

@authorization_ns.route("/test-policy")
class TestUserPolicy(Resource):
    # Resource class for test user policy
    authorization_ns.doc('test_user_policies')
    def post(self):
        message, error = test_policy()
        return message, error
    

@authorization_ns.route("/list-policies")
class ListUserPolicies(Resource):
    # Resource class for listing user policies
    @authorization_ns.doc('list_user_policies')
    @api_key_required
    def post(self):
        policies = list_policies()
        if policies is not None:
            return {"policies": policies}, 200
        else:
            return {"error": "Error al listar las políticas."}, 500



if DEVELOPMENT:
   
    @authentication_ns.route("/register")
    class Register(Resource):
        # Resource class for user registration 
        @authentication_ns.doc('register')
        @authentication_ns.param('username', 'User name', required=True)
        @authentication_ns.param('email', 'User email', required=True)
        @authentication_ns.param('password', 'User password', required=True)
        @authentication_ns.param('password_confirm', 'Password confirmation', required=True)
        def post(self):
            if current_user.is_authenticated:
                return jsonify({"error": "You are already logged in."}), 403
            data = request.get_json()

            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            password_confirm = data.get("password_confirm")

            if not username or not email or not password or not password_confirm:
                return jsonify({"error": "All fields are required."}), 400

            if password != password_confirm:
                return jsonify({"error": "Passwords do not match."}), 400

            
            admin_token = get_x_auth_token(APP_KEYROCK_USERNAME, APP_KEYROCK_PASSWORD)
            headers = {
                'Content-Type': 'application/json',
                'X-Auth-token': admin_token,
            }

            payload = {
                "user": {
                    "username": username,
                    "email": email,
                    "password": password
                }
            }

            response = requests.post(KEYROCK_USERS_URL, json=payload, headers=headers)

            if response.status_code == 201:  # User created successfully
                user_data = response.json()
                user = User(id=user_data["user"]["id"], username=user_data["user"]["username"], email=user_data["user"]["email"])
                db.session.add(user)
                db.session.commit()
                return {"success": "User registered successfully."}, 201
            else:
                # Handle errors returned by Keyrock
                return {"error": f"Error during registration: {response.text}"}, response.status_code

    


    @keyrock_ns.route("/user_from_app/<app_id>")
    class UserFromApp(Resource):
        # Resource class for fetching users based on application ID from Keyrock 
        @keyrock_ns.doc('user_from_app', responses={200: ('OK')})
        @keyrock_ns.param('app_id', 'The ID of the app to fetch')
        def get(self, app_id):
            url = f'{KEYROCK_APPLICATION_URL_1}/{app_id}/{KEYROCK_APPLICATION_URL_2}'
            x_auth_token = get_x_auth_token(APP_KEYROCK_USERNAME, APP_KEYROCK_PASSWORD)
            headers = {
                'X-Auth-token': x_auth_token
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return jsonify(response.json())
            else:
                return jsonify({'error': 'Unable to get users from Keyrock'}), response.status_code
        

    @keyrock_ns.route("/apps")
    class GetApps(Resource):
        # Resource class for fetching all applications from Keyrock 
        @keyrock_ns.doc('get_apps')
        @login_required
        def get(self):
            admin_token = get_x_auth_token(APP_KEYROCK_USERNAME, APP_KEYROCK_PASSWORD)
            headers = {'X-Auth-token': admin_token}
            keyrock_apps_url = KEYROCK_APPLICATION_URL_1
            response = requests.get(keyrock_apps_url, headers=headers)
            if response.status_code == 200:
                try:
                    apps_data = response.json()["applications"]
                    return {"apps": [{"id": app["id"], "name": app["name"]} for app in apps_data]}, 200
                except Exception as e:
                    return {"error": f"Error processing apps from Keyrock: {str(e)}"}, 500
            else:
                return jsonify({"error": f"Error fetching apps from Keyrock: {response.status_code} - {response.text}"}), response.status_code