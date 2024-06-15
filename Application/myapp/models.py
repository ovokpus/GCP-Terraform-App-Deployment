from django.db import models

class Course(models.Model):
    title = models.TextField()
    author = models.TextField()
    overview = models.TextField()
    image = models.TextField()
    url = models.TextField()