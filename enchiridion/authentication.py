from rest_framework import authentication, exceptions
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import UntypedToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if not raw_token:
            return None

        try:
            UntypedToken(raw_token)
        except (InvalidToken, TokenError) as e:
            raise exceptions.AuthenticationFailed(str(e))

        try:
            user = User.objects.get(id=UntypedToken(raw_token).payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)