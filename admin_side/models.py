from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Restaurant name
    address = models.TextField()  # Full address
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Optional contact number
    cuisine_type = models.CharField(max_length=100, blank=True, null=True)  # Type of cuisine (e.g., Filipino, Seafood)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)  # Average rating (e.g., 4.5)
    price_range = models.CharField(max_length=50, blank=True, null=True)  # Price range (e.g., "₱₱₱")
    opening_hours = models.CharField(max_length=100, blank=True, null=True)  # Opening hours (e.g., "9 AM - 9 PM")
    website = models.URLField(blank=True, null=True)  # Website link
    menu_url = models.URLField(blank=True, null=True)  # Link to the menu
    is_open = models.BooleanField(default=True)  # Whether the restaurant is currently open
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update
    photo = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)  # Photo upload

    def __str__(self):
        return self.name
    

