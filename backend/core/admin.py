from django.contrib import admin
from .models import ParkingSpot, ParkingBooking, ParkingVehicle

@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ["spot_id", "zone", "spot_type", "floor", "rate_per_hour", "created_at"]
    list_filter = ["spot_type", "status"]
    search_fields = ["spot_id", "zone", "floor"]

@admin.register(ParkingBooking)
class ParkingBookingAdmin(admin.ModelAdmin):
    list_display = ["spot_id", "vehicle_number", "driver_name", "driver_phone", "entry_time", "created_at"]
    list_filter = ["status"]
    search_fields = ["spot_id", "vehicle_number", "driver_name"]

@admin.register(ParkingVehicle)
class ParkingVehicleAdmin(admin.ModelAdmin):
    list_display = ["vehicle_number", "owner_name", "vehicle_type", "phone", "visits", "created_at"]
    list_filter = ["vehicle_type", "pass_type"]
    search_fields = ["vehicle_number", "owner_name", "phone"]
