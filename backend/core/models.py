from django.db import models

class ParkingSpot(models.Model):
    spot_id = models.CharField(max_length=255)
    zone = models.CharField(max_length=255, blank=True, default="")
    spot_type = models.CharField(max_length=50, choices=[("standard", "Standard"), ("compact", "Compact"), ("handicap", "Handicap"), ("ev_charging", "EV Charging"), ("vip", "VIP")], default="standard")
    floor = models.CharField(max_length=255, blank=True, default="")
    rate_per_hour = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("occupied", "Occupied"), ("reserved", "Reserved"), ("maintenance", "Maintenance")], default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.spot_id

class ParkingBooking(models.Model):
    spot_id = models.CharField(max_length=255)
    vehicle_number = models.CharField(max_length=255, blank=True, default="")
    driver_name = models.CharField(max_length=255, blank=True, default="")
    driver_phone = models.CharField(max_length=255, blank=True, default="")
    entry_time = models.DateField(null=True, blank=True)
    exit_time = models.DateField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.spot_id

class ParkingVehicle(models.Model):
    vehicle_number = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255, blank=True, default="")
    vehicle_type = models.CharField(max_length=50, choices=[("car", "Car"), ("bike", "Bike"), ("truck", "Truck"), ("bus", "Bus")], default="car")
    phone = models.CharField(max_length=255, blank=True, default="")
    visits = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pass_type = models.CharField(max_length=50, choices=[("none", "None"), ("monthly", "Monthly"), ("annual", "Annual")], default="none")
    pass_expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.vehicle_number
