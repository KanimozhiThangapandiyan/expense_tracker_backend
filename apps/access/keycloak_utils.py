import requests
from keycloak import KeycloakOpenID
from django.conf import settings

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=settings.KEYCLOAK_VERIFY_SSL
)

#Function to authenticate user
def get_token(email, password):
    try:
        token = keycloak_openid.token(email, password)
        return token
    except Exception as e:
        raise Exception(f"Keycloak Authentication Failed: {e}")

# Function to get Keycloak admin token
def get_admin_token():
    token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    return response.json().get("access_token")

#Function to create user in keycloak
def create_keycloak_user(user, password):
    """Creates a new user in Keycloak."""
    keycloak_token = get_admin_token()
    if not keycloak_token:
        raise Exception("Could not retrieve Keycloak")

    headers = {
        "Authorization": f"Bearer {keycloak_token}",
        "Content-Type": "application/json"
    }

    keycloak_user_data = {
        "username": user.email_id,  # Using email as username in keycloak
        "email": user.email_id,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "enabled": True,
        "credentials": [{
            "type": "password",
            "value": password,
            "temporary": False
        }]
    }

    keycloak_user_url = f"{settings.KEYCLOAK_SERVER_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users"
    response = requests.post(keycloak_user_url, json=keycloak_user_data, headers=headers)

    if response.status_code != 201:
        raise Exception(f"Keycloak Error: {response.json()}")
