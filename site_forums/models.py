from django.db import models
from django.contrib.auth.models import User
    
class LoginUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return(f'{ self.username }')
    
class Claim(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    claimed_at = models.DateTimeField(auto_now_add=True)
    claim_name = models.CharField(max_length=50)
    claimed_for = models.CharField(max_length=50)
    claim_gen_loc = models.CharField(max_length=100)
    claim_desc = models.TextField(max_length=200)

    def __str__(self):
        return self.claim_name