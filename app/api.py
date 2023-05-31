
from flask import Blueprint, request, jsonify
from app.models import  User
from app.utils import add_policy, api_key_required, get_token, get_x_auth_token, list_policies, store_policy_in_ar
from flask_login import current_user, login_required
from app.config import  DEVELOPMENT, KEYROCK_ADMIN_PASSWORD, KEYROCK_ADMIN_USERNAME, KEYROCK_BASE_URL, ORION_IP, ORION_PORT, KEYROCK_REGISTER_URL
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


@context_broker_ns.route("/entity/<entity>")
class GetEntitiesByType(Resource):
    # Resource class for fetching entities by their type
    @context_broker_ns.doc('get_entities_by_type')
    @context_broker_ns.param('entity', 'The type of entity')
    @conditional_decorator(login_required, api_key_required)
    def get(self, entity):
        headers = {
            "Accept": "application/ld+json",
            "fiware-service": "openiot",
            "fiware-servicepath": "/",
        }

        url = f"http://{ORION_IP}:{ORION_PORT}/ngsi-ld/v1/entities?type={entity}"

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
        headers = {
            "Accept": "application/ld+json",
            "fiware-service": "openiot",
            "fiware-servicepath": "/",
        }

        url = f"http://{ORION_IP}:{ORION_PORT}/ngsi-ld/v1/entities/{entity_id}"

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
        headers = {
            "Accept": "application/ld+json",
            "fiware-service": "openiot",
            "fiware-servicepath": "/",
        }

        url = f"http://{ORION_IP}:{ORION_PORT}/ngsi-ld/v1/types"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            entity_types = response.json()
            return {"entity_types": entity_types}, 200
        else:
            return {"error": f"Error al obtener tipos de entidades del Context Broker: {response.status_code} - {response.text}"}, response.status_code




@authorization_ns.route("/store-policy")
class StoreUserPolicy(Resource):
    # Resource class for storing user policy
    @authorization_ns.doc('store_user_policy')
    @authorization_ns.param('entity_type', 'Entity type', required=True)
    @authorization_ns.param('action', 'Action', required=True)
    @authorization_ns.param('allowed_attributes', 'Allowed attributes', required=True)
    @login_required
    def post(self):
        entity_type = request.form.get("entity_type") or request.json.get("entity_type")
        action = request.form.get("action") or request.json.get("action")
        allowed_attributes = request.form.get("allowed_attributes") or request.json.get("allowed_attributes")
        if not (entity_type and action and allowed_attributes):
            return {"error": "Faltan campos obligatorios."}, 400

        policy = add_policy(entity_type, action, allowed_attributes)
        store_policy_in_ar(policy)

        return {"message": "Política almacenada con éxito."}, 201



@authorization_ns.route("/list-policies")
class ListUserPolicies(Resource):
    # Resource class for listing user policies
    @authorization_ns.doc('list_user_policies')
    @login_required
    def get(self):
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

            admin_email = "admin@test.com"
            admin_password = "1234"
            admin_token = get_x_auth_token(admin_email, admin_password)
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

            response = requests.post(KEYROCK_REGISTER_URL, json=payload, headers=headers)

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
            url = f'{KEYROCK_BASE_URL}/v1/applications/{app_id}/users'
            x_auth_token = get_x_auth_token(KEYROCK_ADMIN_USERNAME, KEYROCK_ADMIN_PASSWORD)
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
            admin_token = get_x_auth_token(KEYROCK_ADMIN_USERNAME, KEYROCK_ADMIN_PASSWORD)
            headers = {'X-Auth-token': admin_token}
            keyrock_apps_url = f"{KEYROCK_BASE_URL}/v1/applications" 
            response = requests.get(keyrock_apps_url, headers=headers)
            if response.status_code == 200:
                try:
                    apps_data = response.json()["applications"]
                    return {"apps": [{"id": app["id"], "name": app["name"]} for app in apps_data]}, 200
                except Exception as e:
                    return {"error": f"Error processing apps from Keyrock: {str(e)}"}, 500
            else:
                return jsonify({"error": f"Error fetching apps from Keyrock: {response.status_code} - {response.text}"}), response.status_code