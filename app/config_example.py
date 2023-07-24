# app/config.py


#Mandatory Config related constants
DEVELOPMENT = False #REQUIRED
REQUIRED_KEYROCK_APP_KEY =  False #REQUIRED
P12_FILE_PATH = '' #REQUIRED
P12_FILE_PASS = '' #REQUIRED
USER_EORI = '' #REQUIRED
USER_SERVICE_PROVIDER_EORI = '' #REQUIRED

#Mandataroy Keyrock related constants
KEYROCK_BASE_URL = '' #REQUIRED
KEYROCK_AUTHORIZATION_URL = f'{KEYROCK_BASE_URL}/oauth2/authorize'
KEYROCK_ACCES_TOKEN_URL = f'{KEYROCK_BASE_URL}/oauth2/token'
KEYROCK_TOKEN_URL = f'{KEYROCK_BASE_URL}/v1/auth/tokens'
KEYROCK_USER_INFO_URL = f'{KEYROCK_BASE_URL}/user'
KEYROCK_USERS_URL = f'{KEYROCK_BASE_URL}/v1/users'
KEYROCK_AR_DELEGATION_ENDPOINT = f'{KEYROCK_BASE_URL}/ar/delegation'
KEYROCK_AR_POLICY = f'{KEYROCK_BASE_URL}/ar/policy'
KEYROCK_APPLICATION_URL_1 = f'{KEYROCK_BASE_URL}/v1/applications'
KEYROCK_APPLICATION_URL_2 = 'users'
KEYROCK_LOGOUT = f'{KEYROCK_BASE_URL}/auth/logout'

#Mandatory Kong related constants
KONG_ADMIN_URL = '' #REQUIRED
KONG_ENTITIES_TYPE = f'{KONG_ADMIN_URL}ngsi-ld/v1/entities?type='
KONG_ENTITIES = f'{KONG_ADMIN_URL}ngsi-ld/v1/entities'

#DEVELOPMENT constant or REQUIRED_KEYROCK_APP_KEY constant is set to true fill this constants
APP_KEYROCK_USERNAME = '' #Only fill out the 'APP_KEYROCK_USERNAME constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
APP_KEYROCK_PASSWORD = '' #Only fill out the 'APP_KEYROCK_PASSWORD constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
APP_URL = '' #Only fill out the 'APP_KEYROCK_PASSWORD constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
APP_REDIRECT_URI = f'{APP_URL}/callback' #Only fill out the 'APP_REDIRECT_URI constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
APP_CLIENT_ID = '' #Only fill out the 'APP_CLIENT_ID constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
APP_CLIENT_SECRET = '' #Only fill out the 'APP_CLIENT_SECRET constant' if the REQUIRED_KEYROCK_APP_KEY is set to true.
#Only used if the REQUIRED_KEYROCK_APP_KEY is set to true.
SWAGGER_AUTHORIZATIONS = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Bearer token',
    },
}

#Uncomment, fill and import the following constants only if the 'send_to_context_broker' and 'get_entity_from_context_broker' methods in the utils.py file are uncommented
#ORION_IP = ''
#ORION_PORT = ''