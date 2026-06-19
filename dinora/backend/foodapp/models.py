from django.db import models

class restaurant(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    delivery_time = models.IntegerField()
    address = models.TextField()
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name