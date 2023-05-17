import json
import jwt
from rest_framework.views import APIView
from .models import USER_details,Personal_info,Token
from .serializers import USER_Serializer,Personal_Serializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .backends import EmailBackend
from datetime import datetime, timedelta
import pymongo
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from bson import ObjectId
from .permissions import CustomIsauthenticated
JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02y'
JWT_ACCESS_TOKEN_EXPIRATION = 120
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'


class Register(APIView):
    def post(self, request, format=None):
        serializer = USER_Serializer(data=json.loads(request.body))
        if serializer.is_valid():
            data = serializer.validated_data
            password = data['password']
            hased_password = make_password(password)
            email = data['email']
            existing_user = USER_details.objects.filter(email=email).first()
            if existing_user is not None:
                return JsonResponse({'Message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(password=hased_password)
                return JsonResponse({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'Message': 'User not created'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        data = request.data
        email = data.get('email',None)
        password = data.get('password',None)
        user=EmailBackend.authenticate(self, request, username=email, password=password)
        if user is not None:
            token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRATION)
                }
            # print(user._id)
            access_token = jwt.encode(token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

            refresh_token_payload = {
                'user_id': str(user._id),
                'exp': datetime.utcnow() + timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION)
                }
            refresh_token = jwt.encode(refresh_token_payload, JWT_SECRET_KEY, JWT_ALGORITHM)

            return JsonResponse({
                    "status": "success",
                    "msg": "user successfully authenticated",
                    "token": access_token,
                    "refresh_token": refresh_token
                })
        else:
            return JsonResponse({"message":"invalid data"})
        

# class UserView(APIView):
#     permission_classes = [CustomIsauthenticated]
#     def get(self, request):
#         token = request.data['access_token']
#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
#             print(payload)
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         user = USER_details.objects.get(_id= ObjectId(payload['user_id']))
#         serializer = USER_Serializer(user)
#         return JsonResponse(serializer.data)

class Userdetails(APIView):
    permission_classes = [CustomIsauthenticated]
    def get(self,request):
        user = USER_details.objects.all()
        serializer = USER_Serializer(user,many=True)
        return Response(serializer.data)
    
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['shopping'] 
my_col=mydb['personal_info']

class Personal_View(APIView):
    permission_classes =[CustomIsauthenticated]
    def post(self,request):
        serializer = Personal_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"saved successfully"})
        return Response({"message":"not created"})


    
# class Logoutview(APIView):
#     permission_classes =[CustomIsauthenticated]
#     def post(self, request):
#         tokens = USER_details.filter(user=request.user)
#         for token in tokens:
#             token.objects.get_or_create(token=token)
#             return Response({'message':'Logout Successfully !'},status=status.HTTP_205_RESET_CONTENT)  
    





