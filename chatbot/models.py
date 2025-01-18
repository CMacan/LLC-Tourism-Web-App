from django.db import models

class Inquiry(models.Model):
    category = models.CharField(max_length=255)  # e.g., "Hotels", "Beaches"
    timestamp = models.DateTimeField(auto_now_add=True)

