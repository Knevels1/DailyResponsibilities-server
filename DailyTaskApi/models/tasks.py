from django.db import models


class Task(models.Model):

    user = models.ForeignKey("TaskUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    content = models.CharField(max_length=2500)
    complete = models.BooleanField()