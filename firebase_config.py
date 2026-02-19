import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

def initialize_firebase():
    if not firebase_admin._apps:
        firebase_creds = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

db = initialize_firebase()