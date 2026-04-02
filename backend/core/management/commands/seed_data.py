from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import ParkingSpot, ParkingBooking, ParkingVehicle
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusParking with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusparking.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if ParkingSpot.objects.count() == 0:
            for i in range(10):
                ParkingSpot.objects.create(
                    spot_id=f"Sample {i+1}",
                    zone=f"Sample {i+1}",
                    spot_type=random.choice(["standard", "compact", "handicap", "ev_charging", "vip"]),
                    floor=f"Sample {i+1}",
                    rate_per_hour=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["available", "occupied", "reserved", "maintenance"]),
                )
            self.stdout.write(self.style.SUCCESS('10 ParkingSpot records created'))

        if ParkingBooking.objects.count() == 0:
            for i in range(10):
                ParkingBooking.objects.create(
                    spot_id=f"Sample {i+1}",
                    vehicle_number=f"Sample {i+1}",
                    driver_name=f"Sample ParkingBooking {i+1}",
                    driver_phone=f"+91-98765{43210+i}",
                    entry_time=date.today() - timedelta(days=random.randint(0, 90)),
                    exit_time=date.today() - timedelta(days=random.randint(0, 90)),
                    duration_hours=round(random.uniform(1000, 50000), 2),
                    amount=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["active", "completed", "cancelled"]),
                )
            self.stdout.write(self.style.SUCCESS('10 ParkingBooking records created'))

        if ParkingVehicle.objects.count() == 0:
            for i in range(10):
                ParkingVehicle.objects.create(
                    vehicle_number=f"Sample {i+1}",
                    owner_name=f"Sample ParkingVehicle {i+1}",
                    vehicle_type=random.choice(["car", "bike", "truck", "bus"]),
                    phone=f"+91-98765{43210+i}",
                    visits=random.randint(1, 100),
                    total_spent=round(random.uniform(1000, 50000), 2),
                    pass_type=random.choice(["none", "monthly", "annual"]),
                    pass_expiry=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 ParkingVehicle records created'))
