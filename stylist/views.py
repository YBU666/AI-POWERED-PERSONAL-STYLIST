from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import UserProfile, OutfitSuggestion, OutfitItem
from .forms import UserProfileForm, OutfitRequestForm
from .groq_client import GroqStyleAssistant
from .image_generator import HuggingFaceImageGenerator
import json
import os
from dotenv import load_dotenv
import base64
from django.contrib.auth.models import User

# Load environment variables
load_dotenv()

def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'stylist/login.html')

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def home(request):
    """Home page view"""
    return render(request, 'stylist/home.html')

def about(request):
    """About page view"""
    return render(request, 'stylist/about.html')

@login_required
def profile(request):
    """View for managing user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'stylist/profile.html', {'form': form})

@login_required
def request_outfit(request):
    """View for requesting outfit suggestions"""
    # Get user profile data
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        initial_data = {
            'height': user_profile.height,
            'skin_tone': user_profile.skin_tone,
            'body_type': user_profile.body_type,
        }
    except UserProfile.DoesNotExist:
        initial_data = {}
    
    if request.method == 'POST':
        form = OutfitRequestForm(request.POST)
        if form.is_valid():
            # Get API key from environment variables
            api_key = os.getenv('HUGGINGFACE_API_KEY')
            if not api_key:
                return render(request, 'stylist/request_outfit.html', {
                    'form': form,
                    'error': 'API key not configured. Please contact administrator.'
                })

            # Initialize the image generator with API key
            image_generator = HuggingFaceImageGenerator(api_key)
            
            # Get user profile data for the AI
            profile_data = {
                'gender': form.cleaned_data['gender'],
                'body_type': form.cleaned_data['body_type'],
                'height': form.cleaned_data['height'],
                'skin_tone': form.cleaned_data['skin_tone']
            }

            # Initialize Groq assistant and generate outfit
            stylist = GroqStyleAssistant()
            suggestion = stylist.generate_outfit_suggestion(
                event_type=form.cleaned_data['event_type'],
                climate=form.cleaned_data['climate'],
                style_preference=form.cleaned_data['style_preference'],
                color_preferences=form.cleaned_data.get('color_preference', []),
                user_profile=profile_data
            )
            
            # Create outfit suggestion record
            outfit = OutfitSuggestion(
                user=request.user,
                gender=form.cleaned_data['gender'],
                event_type=form.cleaned_data['event_type'],
                climate=form.cleaned_data['climate'],
                description=suggestion['description']
            )
            outfit.save()
            
            # Create outfit items with generated images
            for item in suggestion['items']:
                # Generate image for the item with gender-specific prompt enhancement
                description = f"{item['description']} for {form.cleaned_data['gender']}"
                image_data, message = image_generator.generate_fashion_image(description)
                
                if not image_data:
                    messages.warning(request, f"Failed to generate image for {item['type']}: {message}")
                
                # Save the image data to a file
                if image_data:
                    from django.core.files.base import ContentFile
                    from pathlib import Path
                    
                    # Create a unique filename
                    filename = f"outfit_{outfit.id}_{item['type']}.png"
                    image_content = ContentFile(base64.b64decode(image_data))
                    
                    outfit_item = OutfitItem.objects.create(
                        outfit=outfit,
                        item_type=item['type'],
                        description=item['description'],
                        shopping_link=f"https://www.amazon.com/s?k={item['shopping_keywords'].replace(' ', '+')}"
                    )
                    outfit_item.image.save(filename, image_content)
                    outfit_item.save()
                else:
                    OutfitItem.objects.create(
                        outfit=outfit,
                        item_type=item['type'],
                        description=item['description'],
                        shopping_link=f"https://www.amazon.com/s?k={item['shopping_keywords'].replace(' ', '+')}",
                        image=None
                    )
            
            messages.success(request, 'Your personalized outfit has been generated!')
            return redirect('view_outfit', outfit_id=outfit.id)
    else:
        form = OutfitRequestForm(initial=initial_data)
    
    return render(request, 'stylist/request_outfit.html', {'form': form})

@login_required
def view_outfit(request, outfit_id):
    """View for displaying a specific outfit suggestion"""
    try:
        outfit = OutfitSuggestion.objects.get(id=outfit_id, user=request.user)
        items = outfit.items.all()
        return render(request, 'stylist/view_outfit.html', {'outfit': outfit, 'items': items})
    except OutfitSuggestion.DoesNotExist:
        messages.error(request, 'Outfit not found!')
        return redirect('dashboard')

@login_required
def dashboard(request):
    """User dashboard view showing all outfit suggestions"""
    outfits = OutfitSuggestion.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'stylist/dashboard.html', {'outfits': outfits})

@login_required
def toggle_favorite(request, outfit_id):
    """Toggle favorite status of an outfit"""
    try:
        outfit = OutfitSuggestion.objects.get(id=outfit_id, user=request.user)
        outfit.is_favorite = not outfit.is_favorite
        outfit.save()
        return redirect('view_outfit', outfit_id=outfit.id)
    except OutfitSuggestion.DoesNotExist:
        messages.error(request, 'Outfit not found!')
        return redirect('dashboard')

@login_required
def delete_outfit(request, outfit_id):
    """Delete an outfit suggestion"""
    try:
        outfit = OutfitSuggestion.objects.get(id=outfit_id, user=request.user)
        # Delete associated images
        for item in outfit.items.all():
            if item.image:
                item.image.delete()
        outfit.delete()
        messages.success(request, 'Outfit deleted successfully!')
    except OutfitSuggestion.DoesNotExist:
        messages.error(request, 'Outfit not found!')
    return redirect('dashboard')

@login_required
def virtual_tryon(request, item_id):
    """View for virtual try-on of outfit items"""
    try:
        # Get the outfit item
        item = OutfitItem.objects.get(id=item_id)
        
        # Check if the item belongs to the user
        if item.outfit.user != request.user:
            messages.error(request, 'Access denied!')
            return redirect('dashboard')
        
        if request.method == 'POST' and request.FILES.get('person_image'):
            # Get the API key
            api_key = os.getenv('HUGGINGFACE_API_KEY')
            if not api_key:
                messages.error(request, 'API key not configured. Please contact administrator.')
                return redirect('view_outfit', outfit_id=item.outfit.id)

            # Initialize the image generator
            image_generator = HuggingFaceImageGenerator(api_key)
            
            # Read and encode the uploaded person image
            person_image = request.FILES['person_image'].read()
            person_base64 = base64.b64encode(person_image).decode('utf-8')
            
            # Get the clothing item image
            with open(item.image.path, 'rb') as f:
                clothing_image = f.read()
            clothing_base64 = base64.b64encode(clothing_image).decode('utf-8')
            
            # Get the clothing description
            clothing_description = item.description
            
            # Perform virtual try-on
            result_image, message = image_generator.virtual_try_on(
                person_base64, 
                clothing_base64,
                clothing_description
            )
            
            if result_image:
                return render(request, 'stylist/virtual_tryon.html', {
                    'item': item,
                    'result_image': result_image,
                    'original_image': clothing_base64,
                    'person_image': person_base64
                })
            else:
                messages.error(request, f'Virtual try-on failed: {message}')
                return redirect('view_outfit', outfit_id=item.outfit.id)
        
        return render(request, 'stylist/virtual_tryon.html', {'item': item})
        
    except OutfitItem.DoesNotExist:
        messages.error(request, 'Item not found!')
        return redirect('dashboard')

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('dashboard')
    return render(request, 'stylist/register.html')
