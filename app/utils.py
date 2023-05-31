import json
import time
import uuid
from functools import wraps
import requests
from app.config import ACCES_TOKEN_URL, AR_DELEGATION_ENDPOINT, CLIENT_ID, CLIENT_SECRET, SERVICE_PROVIDER_EORI, TOKEN_URL, USER_EORI, USER_INFO_URL, ORION_IP, ORION_PORT

from flask import jsonify, request


def generate_urn(entity_type: str) -> str:
    entity_id = uuid.uuid4()
    return f"urn:ngsi-ld:{entity_type}:{entity_id}"


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        if not access_token:
            return {"error": "Access token is missing."}, 401

        headers = {"Authorization": access_token}
        response = requests.get(USER_INFO_URL, headers=headers)
        if response.status_code != 200:
            return {"error": "Access token is invalid."}, 401

        return f(*args, **kwargs)

    return decorated_function




def get_token(username, password):
    if not username or not password:
            return jsonify({"error": "All fields are required."}), 400

    auth = (CLIENT_ID, CLIENT_SECRET)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(ACCES_TOKEN_URL, auth=auth, data=payload, headers=headers)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return jsonify({"error": f"{response.status_code} - {response.text}"}), 400


def get_x_auth_token(username, password):
    if not username or not password:
        return jsonify({"error": "All fields are required."}), 400

    payload = {
        "name": username,
        "password": password
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(TOKEN_URL, json=payload, headers=headers)

    if response.status_code == 201:
        access_token = response.headers.get("x-subject-token")
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    

def send_to_context_broker(entity,agri_farm_data):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "fiware-service": "openiot",
        "fiware-servicepath": "/",
    }
 
    url = f"http://{ORION_IP}:{ORION_PORT}/ngsi-ld/v1/entities"


    entity_id = f"{agri_farm_data['id']}"
    payload = {
        "id": entity_id,
        "type": entity,
    }

    for key, value in agri_farm_data.items():
        payload[key] = value

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in (201, 204):
        print(f"Error sending data to Context Broker: {response.status_code} - {response.text}")
    else:
        print(f"{entity_id} sucessfully submitted: {response.status_code} - {response.text}")
        time.sleep(3)
        get_entity_from_context_broker(entity_id)



def get_entity_from_context_broker(entity_id):
    headers = {
        "Accept": "application/json",
        "fiware-service": "openiot",
        "fiware-servicepath": "/",
    }

    url = f"http://{ORION_IP}:{ORION_PORT}/ngsi-ld/v1/entities/{entity_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Entity found: {response.text}")
    else:
        print(f"Error getting entity from Context Broker: {response.status_code} - {response.text}")
        




def add_policy(entity_type, action, allowed_attributes):
    policy = {
        "delegationEvidence": {
            "notBefore": int(time.time()),
            "notOnOrAfter": 2147483647,
            "policyIssuer": "<SERVICE_PROVIDER_EORI>",
            "target": {
                "accessSubject": USER_EORI,
            },
            "policySets": [
                {
                    "policies": [
                        {
                            "target": {
                                "resource": {
                                    "type": entity_type,
                                    "identifiers": [
                                        "*"
                                    ],
                                    "attributes": allowed_attributes
                                },
                                "actions": [
                                    action
                                ]
                            },
                            "rules": [
                                {
                                    "effect": "Permit"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    return policy


def add_policy_all_users(entity_type, action, allowed_attributes):
    policy = {
        "delegationEvidence": {
            "notBefore": int(time.time()),
            "notOnOrAfter": 2147483647,
            "policyIssuer": SERVICE_PROVIDER_EORI,
            "policySets": [
                {
                    "policies": [
                        {
                            "target": {
                                "resource": {
                                    "type": entity_type,
                                    "identifiers": [
                                        "*"
                                    ],
                                    "attributes": allowed_attributes
                                },
                                "actions": [
                                    action
                                ]
                            },
                            "rules": [
                                {
                                    "effect": "Permit"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    return policy
  

def store_policy_in_ar(policy):
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(ACCES_TOKEN_URL, data=token_data)
    access_token = response.json()['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(AR_DELEGATION_ENDPOINT, headers=headers, data=json.dumps(policy))

    if response.status_code == 201:
        print("Policy stored successfully")
    else:
        print(f"Error storing policy: {response.status_code} - {response.text}")

def list_policies():
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(ACCES_TOKEN_URL, data=token_data)
    access_token = response.json()['access_token']

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(AR_DELEGATION_ENDPOINT, headers=headers)

    if response.status_code == 200:
        policies = response.json()
        return policies
    else:
        print(f"Error listing policies: {response.status_code} - {response.text}")
        return None


def convert_geojson(type_location, location):
    """
    Convert a GeoJSON object to a format that can be used in the NGSI-LD context.

    Parameters:
        type_location (str): The type of the location. e.g. "Polygon", "Point", "LineString", etc.
        location_json (str): The location data as a GeoJSON string.

    Returns:
        A Python list or dictionary representing the converted location data.

    Raises:
        ValueError: If `type_location` is not a supported GeoJSON type.
    """
    if isinstance(location, str):
        if type_location == "Polygon":
            # Convert the string to a list of coordinate pairs
            coordinates = [list(map(float, pair.split(','))) for pair in location.split(';')]
            location = {"coordinates": [coordinates]}  # Wrap the list of coordinates in another list to match the Polygon format
        else:
            raise ValueError(f"String input is only supported for Polygon types, not {type_location}")
    elif isinstance(location["coordinates"], str):
        location["coordinates"] = json.loads(location["coordinates"])

    if type_location == "Polygon":
        return [location["coordinates"]]
    elif type_location in ["Point", "MultiPoint", "LineString", "MultiLineString", "MultiPolygon"]:
        return location["coordinates"]
    elif type_location == "GeometryCollection":
        return location["geometries"]
    else:
        raise ValueError(f"Unsupported location type: {type_location}")
