import jwt
from rest_framework.permissions import IsAuthenticated
from .models import USER_details
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId
JWT_SECRET_KEY = 'django-insecure-6i9o@jxm94t!sao=x%*6yhx9fyht^62ir(wzw5sre^*a%lk02y'
JWT_ACCESS_TOKEN_EXPIRATION = 60
JWT_REFRESH_TOKEN_EXPIRATION = 1440
JWT_ALGORITHM = 'HS256'

# class  CustomIsauthenticated(IsAuthenticated):
#     """
#     Allows access only to authenticated users.
#     """

#     def has_permission(self, request, view):
#         data=request.headers['Authorization']
#         print(data)
#         token=str.replace(str(data), 'Bearer ', '')
#         if token is None:
#             raise AuthenticationFailed({"message":"authorization is invalid"})

#         payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
#         print(payload)
#         user = USER_details.objects.get(_id= ObjectId(payload['user_id']))
#         if user:
#             return True
#         else:
#             return False

class CustomIsauthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users with valid JWT tokens.
    """

    def has_permission(self, request, view):
        try:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            print(payload)
            user = USER_details.objects.get(_id=ObjectId(payload['user_id']))
            print(user,"************")
            return True
        except (KeyError, jwt.exceptions.DecodeError, USER_details.DoesNotExist):
            raise AuthenticationFailed({'message': 'Authorization details are not provided'})