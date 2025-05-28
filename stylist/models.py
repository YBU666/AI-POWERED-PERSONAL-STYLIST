from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """User profile model for storing user details and preferences"""
    SKIN_TONE_CHOICES = [
        ('fair', 'Fair'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('olive', 'Olive'),
        ('tan', 'Tan'),
        ('deep', 'Deep'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('rectangle', 'Rectangle'),
        ('triangle', 'Triangle'),
        ('inverted_triangle', 'Inverted Triangle'),
        ('hourglass', 'Hourglass'),
        ('apple', 'Apple'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONE_CHOICES, blank=True)
    height = models.IntegerField(help_text="Height in cm", null=True, blank=True)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class OutfitSuggestion(models.Model):
    """Model for storing outfit suggestions"""
    EVENT_TYPE_CHOICES = [
        ('casual', 'Casual'),
        ('formal', 'Formal'),
        ('business', 'Business'),
        ('party', 'Party'),
        ('date', 'Date'),
        ('outdoor', 'Outdoor'),
    ]
    
    CLIMATE_CHOICES = [
        ('hot', 'Hot'),
        ('warm', 'Warm'),
        ('mild', 'Mild'),
        ('cool', 'Cool'),
        ('cold', 'Cold'),
        ('rainy', 'Rainy'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('other', 'Other')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outfit_suggestions')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    climate = models.CharField(max_length=20, choices=CLIMATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    is_favorite = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Outfit for {self.event_type} ({self.user.username})"

class OutfitItem(models.Model):
    """Model for individual items in an outfit suggestion"""
    ITEM_TYPE_CHOICES = [
        ('top', 'Top'),
        ('bottom', 'Bottom'),
        ('dress', 'Dress'),
        ('outerwear', 'Outerwear'),
        ('footwear', 'Footwear'),
        ('accessory', 'Accessory'),
    ]
    
    outfit = models.ForeignKey(OutfitSuggestion, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='outfit_items/', blank=True, null=True)
    shopping_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.item_type}: {self.description}"
