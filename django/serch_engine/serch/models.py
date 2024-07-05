from django.db import models

# Create your models here.


class search_data(models.Model):
    title = models.CharField(max_length=50)
    user = models.CharField(max_length=50)
    url = models.TextField()

    def __str__(self):
        return self.title
