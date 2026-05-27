"""
Firebase Configuration Module
Initializes Firebase Admin SDK and provides database utilities
"""

import base64
import json
import os

import firebase_admin
from firebase_admin import credentials, db, auth as firebase_auth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase Credentials Path
FIREBASE_CRED_PATH = os.path.join(os.path.dirname(__file__), 'firebase-private-key.json')

def get_firebase_credentials():
    """Return Firebase credentials from env or local file."""
    json_b64 = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON_B64', '').strip()
    json_raw = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON', '').strip()

    if json_b64:
        decoded = base64.b64decode(json_b64).decode('utf-8')
        return credentials.Certificate(json.loads(decoded))

    if json_raw:
        return credentials.Certificate(json.loads(json_raw))

    return credentials.Certificate(FIREBASE_CRED_PATH)

# Initialize Firebase Admin SDK
def init_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            cred = get_firebase_credentials()
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
            })
            print("✓ Firebase Admin SDK initialized successfully")
    except FileNotFoundError:
        print("⚠ Warning: firebase-private-key.json not found. Some features may not work.")
        print("  Please download the Service Account Key from Firebase Console.")
    except json.JSONDecodeError:
        print("✗ Error initializing Firebase: invalid service account JSON")
        print("  Check FIREBASE_SERVICE_ACCOUNT_JSON or FIREBASE_SERVICE_ACCOUNT_JSON_B64")
    except Exception as e:
        print(f"✗ Error initializing Firebase: {str(e)}")

# Firebase Web Config (for frontend)
FIREBASE_WEB_CONFIG = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
}

# Initialize on import
init_firebase()

def get_firebase_ref(path=''):
    """Get Firebase Realtime Database reference"""
    try:
        if path:
            return db.reference(path)
        return db.reference()
    except Exception as e:
        print(f"Error getting Firebase reference: {str(e)}")
        return None

def verify_firebase_token(token):
    """
    Verify Firebase ID token with comprehensive error handling
    
    Args:
        token: Firebase ID token
        
    Returns:
        dict: Decoded token if valid, None if invalid
        
    Raises:
        Exception: On token verification errors
    """
    try:
        if not token or not isinstance(token, str):
            raise ValueError("Token must be a non-empty string")
        
        print(f"🔑 Using Firebase app: {firebase_admin._apps if hasattr(firebase_admin, '_apps') else 'ERROR'}")
        print(f"📝 Token type: {type(token)}, Length: {len(token)}")
        
        # Verify token (allow small clock skew to handle minor time drift)
        clock_skew_seconds = int(os.getenv('FIREBASE_CLOCK_SKEW_SECONDS', '60'))
        decoded_token = firebase_auth.verify_id_token(
            token,
            clock_skew_seconds=clock_skew_seconds
        )
        
        print(f"✅ Token decoded successfully")
        print(f"📊 Token claims - UID: {decoded_token.get('uid')}, Email: {decoded_token.get('email')}")
        
        return decoded_token
        
    except firebase_auth.InvalidIdTokenError as e:
        print(f"Invalid ID token: {str(e)}")
        raise ValueError(f"Invalid ID token: {str(e)}")
        
    except firebase_auth.ExpiredIdTokenError as e:
        print(f"Expired ID token: {str(e)}")
        raise ValueError(f"Token has expired. Please login again.")
        
    except firebase_auth.RevokedIdTokenError as e:
        print(f"Revoked ID token: {str(e)}")
        raise ValueError(f"Token has been revoked. Please login again.")
        
    except Exception as e:
        print(f"❌ Token verification error: {type(e).__name__}: {str(e)}")
        raise Exception(f"Token verification failed: {str(e)}")
