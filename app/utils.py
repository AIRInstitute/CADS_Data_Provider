import json
import time
import uuid
from functools import wraps
import requests
from app.config import DATA_MODEL_JSON_LD, KEYROCK_ACCES_TOKEN_URL, KEYROCK_AR_DELEGATION_ENDPOINT, KEYROCK_AR_POLICY, APP_CLIENT_ID, APP_CLIENT_SECRET, KONG_ENTITIES, P12_FILE_PASS, P12_FILE_PATH, REQUIRED_KEYROCK_APP_KEY, USER_SERVICE_PROVIDER_EORI, KEYROCK_TOKEN_URL, USER_EORI, KEYROCK_USER_INFO_URL, USER_EORI
import jwt
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from cryptography.hazmat.primitives import serialization


from flask import jsonify, request


def generate_urn(entity_type: str) -> str:
    entity_id = uuid.uuid4()
    return f"urn:ngsi-ld:{entity_type}:{entity_id}"


def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if(REQUIRED_KEYROCK_APP_KEY is True):
            access_token = request.headers.get("Authorization")
            if not access_token:
                return {"error": "Access token is missing."}, 401

            headers = {"Authorization": access_token}
            response = requests.get(KEYROCK_USER_INFO_URL, headers=headers)
            if response.status_code != 200:
                return {"error": "Access token is invalid."}, 401

            return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return decorated_function




def get_token(username, password):
    if not username or not password:
            return jsonify({"error": "All fields are required."}), 400

    auth = (APP_CLIENT_ID, APP_CLIENT_SECRET)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }

    response = requests.post(KEYROCK_ACCES_TOKEN_URL, auth=auth, data=payload, headers=headers)

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

    response = requests.post(KEYROCK_TOKEN_URL, json=payload, headers=headers)

    if response.status_code == 201:
        access_token = response.headers.get("x-subject-token")
        return access_token
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def p12_read(filepath, password):
    # Leer el archivo PKCS12
    with open(filepath, 'rb') as f:
        p12_data = f.read()

    # Cargar clave privada, certificado y CA certs
    private_key, certificate, ca_certs = load_key_and_certificates(p12_data, password.encode())

    # Convertir la clave privada a formato PEM
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

    # Convertir el certificado a formato PEM
    certificate_pem = certificate.public_bytes(encoding=serialization.Encoding.PEM).decode()

    # Convertir los certificados de CA a formato PEM
    ca_certs_pem = [ca_cert.public_bytes(encoding=serialization.Encoding.PEM).decode() for ca_cert in ca_certs]

    return certificate_pem, private_key_pem, ca_certs_pem


def x5c_read(certificate_pem):  

    # Convertir PEM a base64 (eliminar encabezado y pie de página y juntar líneas)
    b64_cert = certificate_pem.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")

    # El campo x5c contiene el certificado en base64
    x5c = [b64_cert]
    
    return x5c




def get_token_with_jwt():
    certificate, private_key, ca_certs = p12_read(P12_FILE_PATH, P12_FILE_PASS)
    #print("Certificate:", certificate)
    #print("Private Key:", private_key)
    #print("CA Certificates:", ca_certs)

    x5c = x5c_read(certificate)

    header = {
        "typ": "JWT",
        "x5c": x5c
    }

    iss = USER_EORI
    sub = USER_EORI
    aud = USER_EORI
    jti = str(uuid.uuid1())
    iat = int(time.time())
    exp = iat + 30

    payload = {
        "iss": iss,
        "sub": sub,
        "aud": aud,
        "jti": jti,
        "iat": iat,
        "exp": exp
    }

    client_assertion = jwt.encode(payload, private_key, headers=header, algorithm="RS256")
    post_headers = {"Content-type": "application/x-www-form-urlencoded"}

    post_parameters = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "scope": "iSHARE",
        "client_id": USER_EORI,
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": client_assertion
    }

    response = requests.post(KEYROCK_ACCES_TOKEN_URL, headers=post_headers, data=post_parameters)
    if response.status_code in (200, 201, 202):
        access_token = response.json()["access_token"]
        return access_token
    else:
        print(f"Error: {response.status_code}")
        return jsonify({"error": f"{response.status_code} - {response.text}"}), 400

'''
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
'''        

def get_entity_from_kong(entity_id):
    '''headers = {
        "Accept": "application/json",
        "fiware-service": "openiot",
        "fiware-servicepath": "/",
    }'''
    token = get_token_with_jwt()
    headers = {
        "Authorization" : f'Bearer {token}',
        "Content-Type" :  "application/json"
    }
    url = f"{KONG_ENTITIES}/{entity_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Entity found: {response.text}")
    else:
        print(f"Error getting entity from Kong: {response.status_code} - {response.text}")


def send_to_kong(entity, agri_farm_data):
    token = get_token_with_jwt()
    headers = {
        "Authorization" : f'Bearer {token}',
        "Content-Type" :  "application/json",
        "Link": f'<{DATA_MODEL_JSON_LD}>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }
    print( headers)
 
    url = f"{KONG_ENTITIES}"
    entity_id = f"{agri_farm_data['id']}"
    payload = {
        "id": entity_id,
        "type": entity,
    }

    for key, value in agri_farm_data.items():
        payload[key] = value

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in (201, 204):
        print(f"Error sending data to Kong: {response.status_code} - {response.text}")
    else:
        print(f"{entity_id} sucessfully submitted: {response.status_code} - {response.text}")
        time.sleep(3)
        get_entity_from_kong(entity_id)


def add_policy(entity_type, action, allowed_attributes):
    policy = {
        "delegationEvidence": {
            "notBefore": int(time.time()),
            "notOnOrAfter": 2147483647,
            "policyIssuer": USER_SERVICE_PROVIDER_EORI,
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
            "policyIssuer": USER_SERVICE_PROVIDER_EORI,
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
    access_token = get_token_with_jwt()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(KEYROCK_AR_DELEGATION_ENDPOINT, headers=headers, data=json.dumps(policy))

    if response.status_code == 200:
        return {"message": "Policy stored"}, 200

    else:
        return {"error": f"Error storing policy: {response.status_code} - {response.text}"}, 400

def list_policies():
    access_token = get_token_with_jwt()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(KEYROCK_AR_DELEGATION_ENDPOINT, headers=headers)

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


def test_policy():
    access_token = get_token_with_jwt()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    post_data = {
                "delegationEvidence":{
                    "notBefore":1686678252,
                    "notOnOrAfter":1718300617,
                    "policyIssuer":"EU.EORI.ES64973164978542",
                    "target":{
                        "accessSubject":"EU.EORI.ES64973164978542"
                    },
                    "policySets":[
                        {
                            "maxDelegationDepth":2,
                            "target":{
                            "environment":{
                                "licenses":[
                                    "ISHARE.0001",
                                    "ISHARE.0003", "EU.EORI.ES64973164978542"
                                ]
                            }
                            },
                            "policies":[
                            {
                                "target":{
                                    "resource":{
                                        "type":"AgriFarm",
                                        "identifiers":[
                                        "*"
                                        ],
                                        "attributes":[
                                        "*"
                                        ]
                                    },
                                    "actions":[
                                        "POST"
                                    ]
                                },
                                "rules":[
                                    {
                                        "effect":"Permit"
                                    }
                                ]
                            }
                            ]
                        }
                    ]
                }
                }
    response = requests.post(KEYROCK_AR_POLICY, headers=headers, data=post_data)
    if response.status_code == 200:
        return {"message": "Policy stored"}, 200

    else:
        return {"error": f"Error storing policy: {response.status_code} - {response.text}"}, 400