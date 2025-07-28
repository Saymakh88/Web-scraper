from django.db import models


# Create your models here.
class Link(models.Model):

    def __str__(self):
        return str(self.name) 
    
    address=models.CharField(max_length=1000,null=True,blank=True)
    name=models.CharField(max_length=1000,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # to track time