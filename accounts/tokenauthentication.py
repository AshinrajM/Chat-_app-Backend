import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

# here we use settings secret for encrypting the token ie, why here we imported settings

User = get_user_model()


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = self.extract_token(request)
        if token is None:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            self.verify_token(payload=payload)

            user_id = payload["id"]
            user = User.objects.get(id=user_id)
            return (user, None)  # Return a tuple containing the user object and None
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("invalid token")

    def verify_token(self, payload):
        if "exp" not in payload:
            raise InvalidTokenError("token has no expiration")

        exp_timestamp = payload["exp"]
        current_timestamp = datetime.utcnow().timestamp()
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        auth_header = request.headers.get("Authorization")
        # this auth header will be a string, where string will starts with 'Bearer ' we will split it with space given
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    # this function  below will be static function , this will be same for every object we create thats why we use this decorator
    @staticmethod
    def generate_token(payload):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload["exp"] = expiration
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token
