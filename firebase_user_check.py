import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Test read from 'users' collection
users_ref = db.collection('users')
docs = users_ref.stream()

print("Registered Users and Their Markets:")
for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

