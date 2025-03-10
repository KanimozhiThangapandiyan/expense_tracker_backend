import requests
from keycloak import KeycloakOpenID
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=settings.KEYCLOAK_VERIFY_SSL
)

def get_token(email, password):
    """Function to authenticate user using Keycloak."""
    try:
        token = keycloak_openid.token(email, password)
        return token
    except Exception as e:
        raise Exception(f"Keycloak Authentication Failed: {e}")

def get_admin_token():
    """Function to get the admin token for Keycloak."""
    token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=data)
    return response.json().get("access_token")

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
       
def get_new_access_token(refresh_token):
    """ Function to refresh the access token using the refresh token."""

    token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return tokens["access_token"], tokens.get("refresh_token")
    else:
        return None, response.json().get("error_description", "Failed to refresh token")

class KeycloakUser:
    """Custom user object to attach user info."""
    def __init__(self, user_info):
        self.user_info = user_info
        self.username = user_info.get("preferred_username", "")
        self.email = user_info.get("email", "")
        self.is_authenticated = True

    def __str__(self):
        return self.username

class KeycloakAuthentication(BaseAuthentication):
    """Custom authentication class to authenticate users using Keycloak."""
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        try:
            user_info = keycloak_openid.userinfo(token) # Get user info from token
            return (KeycloakUser(user_info), None)  # Attach user info to request.user
        except Exception:
            raise AuthenticationFailed("Invalid or expired token")