from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='users-register'),
    path('profile/', views.profile, name='users-profile'),
    path('profile/update/', views.update_profile, name='users-update-profile'),
    path('delete-account/', views.delete_account, name='users-delete-account'),
]
