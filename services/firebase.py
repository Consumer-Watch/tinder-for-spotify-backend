from config.firebase import default_app
from firebase_admin import firestore, storage

class Firebase:
    firebase_app = default_app

    bucket = storage.bucket("sonder-bucket", firebase_app)

    @classmethod
    def add_to_firestore(cls, data: any):
        firestore.client(cls.firebase_app).collection("test-collection").add({
            "hello": "world"
        })

    @classmethod
    def add_to_storage(cls, path: str, uri: str):
        cls.bucket.blob(path).upload_from_string(uri)

