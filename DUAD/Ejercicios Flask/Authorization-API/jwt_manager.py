import jwt
from datetime import datetime, timedelta, timezone


class JWTManager:
    def __init__(self, private_key, public_key, algorithm, access_expiration, refresh_expiration):
        self.private_key = private_key
        self.public_key = public_key
        self.algorithm = algorithm
        self.access_expiration = access_expiration
        self.refresh_expiration = refresh_expiration

    def encode(self, data, expires_in):
        payload = {
            **data,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
        }
        try:
            return jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        except (jwt.PyJWTError, TypeError) as error:
            print(f"Error generating token: {error}")
            return None

    def decode(self, token):
        try:
            return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        except jwt.PyJWTError as error:
            print(f"Invalid token: {error}")
            return None

    def generate_tokens(self, user_id):
        access_token = self.encode({"id": user_id, "type": "access"}, self.access_expiration)
        refresh_token = self.encode({"id": user_id, "type": "refresh"}, self.refresh_expiration)
        return access_token, refresh_token

    def decode_token(self, token, expected_type):
        decoded = self.decode(token)
        # A valid token of the wrong type is rejected just like an invalid one
        if decoded is None or decoded.get("type") != expected_type:
            return None
        return decoded


ACCESS_TOKEN_EXPIRATION = 60 * 15  # 15 minutes
REFRESH_TOKEN_EXPIRATION = 60 * 60 * 24 * 7  # 7 days

with open("private_key.pem", "rb") as private_key_file:
    PRIVATE_KEY = private_key_file.read()

with open("public_key.pem", "rb") as public_key_file:
    PUBLIC_KEY = public_key_file.read()

jwt_manager = JWTManager(
    private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY,
    algorithm="RS256",
    access_expiration=ACCESS_TOKEN_EXPIRATION,
    refresh_expiration=REFRESH_TOKEN_EXPIRATION,
)
