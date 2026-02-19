from firebase_config import db
from datetime import datetime

def save_scan(user_id, product_text, ai_result):
    doc = {
        "product_text": product_text,
        "ai_result": ai_result,
        "timestamp": datetime.now()
    }
    db.collection("users").document(user_id).collection("scans").add(doc)
    print("✅ Scan saved to Firebase!")

def get_scan_history(user_id):
    scans = db.collection("users").document(user_id).collection("scans")\
               .order_by("timestamp").stream()
    return [s.to_dict() for s in scans]