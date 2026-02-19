import firebase_admin
from firebase_admin import credentials, firestore, storage

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'beforeyoubuy-d8bd1.appspot.com'
        })
    db = firestore.client()
    return db

db = initialize_firebase()