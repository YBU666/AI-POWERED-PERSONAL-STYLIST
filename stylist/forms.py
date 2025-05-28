from django import forms
from .models import UserProfile, OutfitSuggestion

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    class Meta:
        model = UserProfile
        fields = ['skin_tone', 'height', 'body_type', 'profile_image']
        widgets = {
            'height': forms.NumberInput(attrs={'placeholder': 'Height in cm'}),
        }

class OutfitRequestForm(forms.Form):
    """Form for requesting outfit suggestions"""
    EVENT_TYPE_CHOICES = OutfitSuggestion.EVENT_TYPE_CHOICES
    CLIMATE_CHOICES = OutfitSuggestion.CLIMATE_CHOICES
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('other', 'Other')
    ]
    
    # Personal Information
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        help_text="Select your gender for better outfit recommendations"
    )
    height = forms.IntegerField(
        required=False,
        help_text="Your height in cm",
        widget=forms.NumberInput(attrs={'placeholder': 'Height in cm'})
    )
    skin_tone = forms.ChoiceField(
        choices=UserProfile.SKIN_TONE_CHOICES,
        required=False,
        help_text="Select your skin tone for color-coordinated outfits"
    )
    body_type = forms.ChoiceField(
        choices=UserProfile.BODY_TYPE_CHOICES,
        required=False,
        help_text="Select your body type for better fitting suggestions"
    )
    
    # Event and Style Preferences
    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, required=True)
    climate = forms.ChoiceField(choices=CLIMATE_CHOICES, required=True)
    style_preference = forms.ChoiceField(
        choices=[
            ('casual', 'Casual'),
            ('classic', 'Classic'),
            ('bohemian', 'Bohemian'),
            ('streetwear', 'Streetwear'),
            ('minimalist', 'Minimalist'),
            ('vintage', 'Vintage'),
        ],
        required=True
    )
    color_preference = forms.MultipleChoiceField(
        choices=[
            ('neutral', 'Neutral tones'),
            ('bright', 'Bright colors'),
            ('pastel', 'Pastel colors'),
            ('dark', 'Dark colors'),
            ('monochrome', 'Monochrome'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Any additional preferences or requirements"
    )
