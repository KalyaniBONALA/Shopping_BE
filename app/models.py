from django.db import models
from djongo import models

class USER_details(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    usertype = models.CharField(max_length=20,editable=True)
    username = models.CharField(max_length=138)
    email = models.EmailField()
    password = models.CharField(max_length=138)
    date_joined = models.DateTimeField(auto_now_add=True)

GENDER =(
    ('Male','male'),
    ('Female','female'),
)
class Personal_info(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    username = models.CharField(max_length=138)
    email = models.EmailField()
    gender = models.CharField(max_length=200,choices=GENDER)
     

class Token(models.Model):
    _id=models.ObjectIdField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.CharField(max_length=200)
    token = models.CharField(max_length=700)
    