from django.db import models

class DataPoint(models.Model):
    x_value = models.CharField(max_length=100)
    y_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default='manual')

    def __str__(self):
        return f"{self.x_value}: {self.y_value}"