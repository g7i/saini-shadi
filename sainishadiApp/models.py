from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):

    GENDER = (
        ('Male','Male'),
        ('Female','Female'),
    )

    JOB = (
        ('self','Self'),
        ('pvt','PVT'),
    )

    MANGLIK = (
        ('Yes','Yes'),
        ('No','No'),
    )

    STATUS = (
        ('Unmarried','Unmarried'),
        ('Divorced','Divorced'),
    )


    COLOUR = (
        ('Fair','Fair'),
        ('Medium','Medium'),
        ('Dark','Dark'),
    )

    PHY = (
        ('Fat','Fat'),
        ('Average','Average'),
        ('Slim','Slim'),
    )

    father_name = models.CharField(max_length=50,default='',blank=True)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=6,choices=GENDER,default='',blank=True)
    status = models.CharField(max_length=10,choices=STATUS,default='',blank=True)
    mobile = models.CharField(max_length=15,default='',blank=True)
    address = models.TextField(default='',blank=True)
    manglik = models.CharField(max_length=3,choices=MANGLIK,default='',blank=True)
    self_gotra = models.CharField(max_length=20,default='',blank=True)
    mother_gotra = models.CharField(max_length=20,default='',blank=True)
    nani_gotra = models.CharField(max_length=20,default='',blank=True)
    dadi_gotra = models.CharField(max_length=20,default='',blank=True)
    edu = models.TextField(default='',blank=True)
    job_type = models.CharField(max_length=15,choices=JOB,default='',blank=True)
    job_desc = models.CharField(max_length=100,default='',blank=True)
    publish = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',default='images/0.png')
    drink = models.CharField(max_length=3,choices=MANGLIK,default='',blank=True)
    smoking  = models.CharField(max_length=3,choices=MANGLIK,default='',blank=True)
    height_foot = models.IntegerField(null=True,blank=True)
    height_inch = models.IntegerField(null=True,blank=True)
    colour = models.CharField(max_length=6,choices=COLOUR,default='',blank=True)
    physique = models.CharField(max_length=7,choices=PHY,default='',blank=True)
    registered =  models.BooleanField(default=False)
    published =  models.BooleanField(default=False)
    city =  models.CharField(max_length=20,default='',blank=True)
    state =  models.CharField(max_length=20,default='',blank=True)

    @property
    def age(self):
        try:
            return int(round((datetime.now().date() - self.dob).days / 365.25))
        except:
            return '-'

class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=10,default='No')
    
    def __str__(self):
        return self.user.username+' '+self.status