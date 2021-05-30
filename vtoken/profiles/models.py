from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER = [
        ('M','Male'),
        ('F','Female'),
        ('PNS','Prefer Not To Say'),
        ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50, blank=True)
    website = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=3, choices = GENDER,default='PNS')
    dob = models.DateField(null=True,auto_now_add=False, blank=True)
    linkedin = models.CharField(max_length=500, blank=True)
    twitter = models.CharField(max_length=500, blank=True)
    github = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

class Profileimage(models.Model):
    # background_image = models.ImageField(default='default_bg.png', blank=True , upload_to = 'background_images')
    profile_image = models.ImageField(default='default_dp.png', blank=True , upload_to = 'profile_images')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return str(self.user)

class Academicdetails(models.Model):
    COURSE = [
    ('CSE','computer science and engineering'),
    ('IT','information technology'),
    ('ECE','electrical and communications engineering'),
    ('EEE','electrical and electronic engineering'),
    ('Mech', 'mechanical engineering'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    college = models.CharField(max_length=200, blank=True)
    college_id = models.CharField(max_length=10, blank=False)
    course = models.CharField(max_length=5, choices = COURSE,default='CSE')
    year = models.IntegerField(default=1)
