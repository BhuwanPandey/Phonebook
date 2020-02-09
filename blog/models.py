from django.db import models

# Create your models here.
class Phonebook(models.Model):
    name=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    images=models.ImageField(upload_to='images',null=True,blank=True)

    def __str__(self):
        return self.name