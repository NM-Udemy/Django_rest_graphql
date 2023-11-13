from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()
    
    def __str__(self):
        return self.name
    
class Equipment(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    facility = models.ForeignKey(Facility, related_name='equipments',
                                 on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.facility.name}: {self.name}({self.quantity})'

class FacilityType(models.Model):
    name = models.CharField(max_length=100)
    facility = models.ForeignKey(Facility, related_name='facility_types',
                                 on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.facility.name}: {self.name}'


class UserPicture(models.Model):
    image = models.ImageField(upload_to='media/images/')
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    