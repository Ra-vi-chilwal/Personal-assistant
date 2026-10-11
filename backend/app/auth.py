import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me").encode()
TOKEN_TTL = 60 * 60 * 24 * 7  # 7 days

db = MongoClient(os.getenv("MONGODB_URI"))["rag_db"]
users = db["users"]
users.create_index("email", unique=True)

bearer = HTTPBearer(auto_error=False)


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
    return f"{salt}${digest.hex()}"


def verify_password(password, stored):
    salt, _ = stored.split("$", 1)
    return hmac.compare_digest(hash_password(password, salt), stored)


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def create_token(user_id):
    payload = _b64(json.dumps({"sub": user_id, "exp": int(time.time()) + TOKEN_TTL}).encode())
    sig = _b64(hmac.new(SECRET, payload.encode(), hashlib.sha256).digest())
    return f"{payload}.{sig}"


def decode_token(token):
    try:
        payload, sig = token.split(".")
        expected = _b64(hmac.new(SECRET, payload.encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(_unb64(payload))
        return data["sub"] if data["exp"] > time.time() else None
    except Exception:
        return None


def public_user(u):
    return {"id": str(u["_id"]), "name": u["name"], "email": u["email"], "role": u.get("role", "")}


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    from bson import ObjectId

    user_id = decode_token(creds.credentials) if creds else None
    user = users.find_one({"_id": ObjectId(user_id)}) if user_id else None
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user
