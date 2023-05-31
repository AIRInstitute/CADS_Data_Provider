# app/config.py

DEVELOPMENT = True

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:5000/callback'
KEYROCK_BASE_URL = 'http://localhost:3000'
AUTHORIZATION_URL = f'{KEYROCK_BASE_URL}/oauth2/authorize'
ACCES_TOKEN_URL = f'{KEYROCK_BASE_URL}/oauth2/token'
TOKEN_URL = f'{KEYROCK_BASE_URL}/v1/auth/tokens'
USER_INFO_URL = f'{KEYROCK_BASE_URL}/user'
KEYROCK_REGISTER_URL = f'{KEYROCK_BASE_URL}/v1/users'
KEYROCK_ADMIN_USERNAME = ''
KEYROCK_ADMIN_PASSWORD = ''
AUTHZ_REGISTRY_URL = 'http://localhost:7000'
AR_DELEGATION_ENDPOINT = f'{KEYROCK_BASE_URL}/ar/delegation'

#ngsi-ishare-policies KONG
KONG_ADMIN_URL = 'http://localhost:8000'
ROUTE_ID = '/api/users'

PLUGINS_URL =  f'{KONG_ADMIN_URL}/routes/'f'{ROUTE_ID}/plugins'
ROUTES_URL = f'{KONG_ADMIN_URL}/routes'
USER_EORI = ''
SERVICE_PROVIDER_EORI = ''

ORION_IP = 'localhost'
ORION_PORT = 1026


AUTHORIZATIONS = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Bearer token',
    },
}