from django.db import models


class Progress(models.Model):
    food = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

    class Meta:
        app_label = 'test1'
