from rest_framework import serializers
from .models import USER_details,Personal_info

 

class USER_Serializer(serializers.ModelSerializer):
    class Meta:
        model = USER_details
        fields = ['username','email','password','usertype','date_joined']

class Personal_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_info
        fields = ['email','gender','username']

       