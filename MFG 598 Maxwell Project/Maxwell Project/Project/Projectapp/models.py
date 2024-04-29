from django.db import models

# Create your models here.
class SignUp(models.Model):
    firstname=models.TextField(default=None)
    lastname=models.TextField(default=None)
    username=models.TextField(default=None)
    password=models.TextField(default=None)
    confirmpassword=models.TextField(null=True,blank=True,default="0")
    mailbox=models.TextField(null=True,blank=True,default="0")
    