from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Define home route for root URL
    path('run-tracker/', views.run_tracker, name='run_tracker'),  # Your existing tracker route
]