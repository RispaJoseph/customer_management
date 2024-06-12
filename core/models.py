from django.db import models
from django.contrib.auth.models import User 

class Checker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Maker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    checker = models.ForeignKey(Checker, related_name='makers', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    DECLINED = 'Declined'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    ]

    maker = models.ForeignKey(Maker, related_name='customers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/')
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.name
