import base64
import hashlib
import secrets
import string
import urllib.parse
import requests
from typing import Tuple, Dict

class OAuth2Utils:
    def __init__(self):
        self.client_id = 'JrA9YLISRey0xThqT7gLAINqFhyVJntqWnn9OOMz'
        self.client_secret = 'pbkdf2_sha256$870000$3ekR17enNKKeT8gMOnXRQm$FAXHgq1B2nluLghxeNFKql4yjK6O/1ehdXK7O/oT6d8='
        self.redirect_uri = 'http://127.0.0.1:8000/noexist/callback'
        self.token_endpoint = 'http://127.0.0.1:8000/o/token/'
        self.auth_endpoint = 'http://127.0.0.1:8000/o/authorize/'

    def exchange_code_for_token(self, code: str, code_verifier: str) -> Dict:
        """Exchange authorization code for access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'code_verifier': code_verifier,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(self.token_endpoint, data=data, headers=headers)
        return response.json()

    def generate_pkce_pair(self, length: int = 128) -> Tuple[str, str]:
        """Generate PKCE code verifier and challenge pair"""
        code_verifier = ''.join(secrets.choice(
            string.ascii_letters + string.digits + "-._~"
        ) for _ in range(length))
        
        code_challenge = hashlib.sha256(code_verifier.encode('ascii')).digest()
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('ascii').replace('=', '')
        
        return code_verifier, code_challenge

    def get_authorization_url(self, code_challenge: str) -> str:
        """Build OAuth2 authorization URL with PKCE"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        return f"{self.auth_endpoint}?{urllib.parse.urlencode(params)}"

# Step 1: Generate the PKCE Pair
oauth2 = OAuth2Utils()
code_verifier, code_challenge = oauth2.generate_pkce_pair()

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")

# Step 2: Get the Authorization URL
auth_url = oauth2.get_authorization_url(code_challenge)
print(f"Authorization URL: {auth_url}")
