from django.db import models
from django.db.models import Avg
import math

def precise_round(value):
    if value is None:
        return 0
    decimal = value - int(value)
    if decimal <= 0.5:
        return math.ceil(value)
    else:
        return math.floor(value)
    
# Create your models here.
class Professor(models.Model):
    professor_id = models.CharField(max_length=10, primary_key=True)
    professor_name = models.CharField(max_length=30)
    #average_rating = models.ForeignKey('CachedRating', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.professor_name}"
    
class Module(models.Model):    
    module_code = models.CharField(max_length=10, primary_key=True, unique=True) #each module code is unique
    module_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.module_name

SEMESTERS = [(1, '1'), (2, '2')]

class ModuleInstance(models.Model):
    module_instance_id = models.AutoField(primary_key=True)
    semester = models.IntegerField(choices=SEMESTERS) #only allow 2 choices for 2 semesters
    year = models.IntegerField()
    professors = models.ManyToManyField(Professor) #A module can be taught by many professors
    module = models.ForeignKey(Module, on_delete=models.PROTECT) #A module instance can only have one module
    
    def __str__(self):
        return f"{self.module.module_code} - {self.year} - Semester {self.semester}"
    
RATINGS = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
       
class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating = models.IntegerField(choices=RATINGS)
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.PROTECT) #A rating can only be associated with one module instance
    user = models.CharField(max_length=30)
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT) #A rating can only be associated with one professor
    #create a fucntion to overide the create function in views.py
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        avg_rating = Rating.objects.filter(professor=self.professor).aggregate(Avg("rating"))['rating__avg']# get all ratings for that professor and calculate the average
        avg_rating = precise_round(avg_rating) if avg_rating else 0
        
        cached_average, created = CachedRating.objects.get_or_create(professor=self.professor)
        cached_average.average_rating = avg_rating
        cached_average.save()
            
        #send the average rating to the professor table
        #professor_average = Professor.objects.get_or_create(professor=self.professor)
        self.professor.average_rating = avg_rating
        self.professor.save()     
    
    def __str__(self):
        return f"{self.rating} for {self.professor} in {self.module_instance}"
    
#create new table to store current ratings, when we press view it should fetch avg from this table
class CachedRating(models.Model):
    
    average_rating = models.FloatField(default=0)
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE)
        
    def __str__(self):
        return f"Cached Rating: {self.professor} - {self.average_rating}"    
        
    