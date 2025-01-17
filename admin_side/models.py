from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  
    description = models.TextField()
    image = models.ImageField(upload_to='destination_images/')
    category = models.CharField(max_length=50, choices=[
        ('Beach', 'Beach'),
        ('Mountain', 'Mountain'),
        ('City', 'City'),
        ('Cultural', 'Cultural'),
    ])
    rating = models.IntegerField()
    popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def google_maps_link(self):
        """Returns the Google Maps URL."""
        if self.latitude and self.longitude:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        elif self.location:
            return f"https://www.google.com/maps?q={self.location}"
        return None
    
class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)  # For example, 2 hours
    image = models.ImageField(upload_to='activity/', null=True, blank=True)
    category = models.CharField(max_length=100, choices=[('adventure', 'Adventure'), ('relaxation', 'Relaxation'), ('cultural', 'Cultural'), ('educational', 'Educational')])
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='accommodations/', null=True, blank=True)
    amenities = models.JSONField(null=True, blank=True)  # Example: ["WiFi", "Pool", "Breakfast"]
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-rating']
        verbose_name_plural = 'Accommodations'

class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Restaurant name
    address = models.TextField()  # Full address
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)  # Average rating (e.g., 4.5)
    opening_hours = models.CharField(max_length=100, blank=True, null=True)  # Opening hours (e.g., "9 AM - 9 PM")
    website = models.URLField(blank=True, null=True)  # Website link
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update
    image = models.ImageField(upload_to='restaurant_photos/', blank=True, null=True)  # Photo upload

    def __str__(self):
        return self.name
    

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)  # Example: "Travel, Tips, Beach"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

