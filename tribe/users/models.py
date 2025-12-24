from django.db import models

# Create your models here.

class profile(models.Model):
    display_name=models.CharField(max_length=100)
    bio=models.CharField(max_length=100)
    pfp=models.ImageField()
    
    def __str__(self):
        return self.name