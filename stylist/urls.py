from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('request-outfit/', views.request_outfit, name='request_outfit'),
    path('outfit/<int:outfit_id>/', views.view_outfit, name='view_outfit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('toggle-favorite/<int:outfit_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('delete-outfit/<int:outfit_id>/', views.delete_outfit, name='delete_outfit'),
    path('virtual-tryon/<int:item_id>/', views.virtual_tryon, name='virtual_tryon'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]

# Add media URL patterns for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
