from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('parkingspots/', views.parkingspot_list, name='parkingspot_list'),
    path('parkingspots/create/', views.parkingspot_create, name='parkingspot_create'),
    path('parkingspots/<int:pk>/edit/', views.parkingspot_edit, name='parkingspot_edit'),
    path('parkingspots/<int:pk>/delete/', views.parkingspot_delete, name='parkingspot_delete'),
    path('parkingbookings/', views.parkingbooking_list, name='parkingbooking_list'),
    path('parkingbookings/create/', views.parkingbooking_create, name='parkingbooking_create'),
    path('parkingbookings/<int:pk>/edit/', views.parkingbooking_edit, name='parkingbooking_edit'),
    path('parkingbookings/<int:pk>/delete/', views.parkingbooking_delete, name='parkingbooking_delete'),
    path('parkingvehicles/', views.parkingvehicle_list, name='parkingvehicle_list'),
    path('parkingvehicles/create/', views.parkingvehicle_create, name='parkingvehicle_create'),
    path('parkingvehicles/<int:pk>/edit/', views.parkingvehicle_edit, name='parkingvehicle_edit'),
    path('parkingvehicles/<int:pk>/delete/', views.parkingvehicle_delete, name='parkingvehicle_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
