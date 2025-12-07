"""
Firebase Configuration Module
Initializes Firebase Admin SDK with credentials from environment variables
"""

import os
import re
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    
    # Get and sanitize private key
    private_key = os.getenv("FIREBASE_PRIVATE_KEY", "")
    # Handle literal newlines from .env
    private_key = private_key.replace('\\n', '\n')
    # Normalize dashes (some copy-pastes have em-dashes)
    private_key = private_key.replace('—', '-').replace('–', '-')
    # Fix header if malformed (e.g. missing dashes or wrong dashes)
    private_key = re.sub(r'^[^\w\n]*BEGIN PRIVATE KEY[^\w\n]*', '-----BEGIN PRIVATE KEY-----', private_key.strip())
    # Fix footer if malformed
    private_key = re.sub(r'[^\w\n]*END PRIVATE KEY[^\w\n]*$', '-----END PRIVATE KEY-----', private_key.strip())

    # Build credentials from environment variables
    firebase_credentials = {
        "type": os.getenv("FIREBASE_TYPE", "service_account"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL")
    }
    
    # Validate required fields
    required_fields = ["project_id", "private_key", "client_email"]
    missing_fields = [field for field in required_fields if not firebase_credentials.get(field)]
    
    if missing_fields:
        raise ValueError(f"Missing required Firebase credentials: {', '.join(missing_fields)}")
    
    # Initialize Firebase
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
    
    return firestore.client()

# Initialize Firestore client
db = initialize_firebase()
