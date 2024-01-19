import os, requests
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.conf import settings
from django.middleware import csrf
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

def create_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token is None:
        return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Create a RefreshToken instance
        token = RefreshToken(refresh_token)
        
        # Check if the token has expired
        token.check_exp()
        token.verify_token_type()
        
        # If the token is valid, return a successful response
        return Response({"valid": True, "id": token.payload['user_id']}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        tokens = create_user_tokens(authenticated_user)
        
        data = {
            "id": authenticated_user.id,
            "valid": True
        }
        response = Response(data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', tokens["refresh"], httponly=True)
        response.set_cookie('access_token', tokens["access"], httponly=True)
        response.set_cookie('csrftoken', csrf.get_token(request), httponly=False)
        return response
    else:
        data = { 'valid': False }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    try:
        check_email = User.objects.filter(email=request.data['email']).first()
        if check_email is not None:
            return Response({ 'error': 'A user with this email already exists.' }, status=status.HTTP_400_BAD_REQUEST)
        
        new_user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['firstName'],
            last_name=request.data['lastName']
        )
        
        data = {
            "id": new_user.id,
            "valid": True
        }

        tokens = create_user_tokens(new_user)
        response = Response(data=data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', tokens["refresh"], httponly=True)
        response.set_cookie('access_token', tokens["access"], httponly=True)
        response.set_cookie('csrftoken', csrf.get_token(request), httponly=False)
        return response
    except IntegrityError:
        return Response({ 'error': 'A user with this username already exists.' }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    # first, we need to take the code from the request and send it to google to get access and refresh tokens
    # then, we need to take the access token and send it to google to get the user's info
    # then, we need to check if the user exists in our database
    # if the user exists, we need to log them in
    # if the user does not exist, we need to create them and log them in
    # finally, we need to return the user's info and a token
    
    code = request.data['codeResponse']
    
    # get access and refresh tokens
    url = 'https://oauth2.googleapis.com/token'
    redirect_uri = os.getenv('CLIENT_URL')
    data = {
        'code': code,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': f'{redirect_uri}/login',
        'grant_type': 'authorization_code'
    }
    
    POST_response = requests.post(url, data=data)
    POST_response = POST_response.json()
    
    # get user info
    url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + POST_response['access_token']
    GET_response = requests.get(url)
    GET_response = GET_response.json()
    
    # check if user exists
    user = User.objects.filter(email=GET_response['email']).first()
    if user is not None:
        data = {
            "id": user.id,
            "valid": True,
        }
        
        tokens = create_user_tokens(user)
        response = Response(data=data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', tokens["refresh"], httponly=True)
        response.set_cookie('access_token', tokens["access"], httponly=True)
        response.set_cookie('csrftoken', csrf.get_token(request), httponly=False)
        return response
    
    # create user
    try:
        new_user = User.objects.create_user(
            username=GET_response['email'],
            email=GET_response['email'],
            first_name=GET_response['given_name'],
            last_name=GET_response['family_name']
        )
        new_user.set_unusable_password()
        new_user.save()
        
        data = {
            "id": new_user.id,
            "valid": True,
        }
        
        tokens = create_user_tokens(new_user)
        response = Response(data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', tokens["refresh"], httponly=True)
        response.set_cookie('access_token', tokens["access"], httponly=True)
        response.set_cookie('csrftoken', csrf.get_token(request), httponly=False)
        return response
    except IntegrityError:
        return Response({ 'error': 'A user with this username already exists.' }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_user(request):
    response = Response(status=status.HTTP_200_OK)
    response.delete_cookie('refresh_token')
    response.delete_cookie('access_token')
    response.delete_cookie('csrftoken')
    return response
