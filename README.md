# Cryptography Virtual Lab

Interactive learning platform for cryptography labs built with Flask and Firebase auth.

## Quick start
1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the app: `python app.py`.

## Notes
- Configure Firebase env vars and the service account before login.
- App runs at http://127.0.0.1:5000 by default.

## Render deploy (minimal)
- Use the included render.yaml.
- Set env vars: SECRET_KEY, FIREBASE_DATABASE_URL, FIREBASE_PROJECT_ID,
  FIREBASE_SERVICE_ACCOUNT_JSON (or FIREBASE_SERVICE_ACCOUNT_JSON_B64),
  FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, FIREBASE_STORAGE_BUCKET,
  FIREBASE_MESSAGING_SENDER_ID, FIREBASE_APP_ID.
