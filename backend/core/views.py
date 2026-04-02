import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import ParkingSpot, ParkingBooking, ParkingVehicle


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['parkingspot_count'] = ParkingSpot.objects.count()
    ctx['parkingspot_standard'] = ParkingSpot.objects.filter(spot_type='standard').count()
    ctx['parkingspot_compact'] = ParkingSpot.objects.filter(spot_type='compact').count()
    ctx['parkingspot_handicap'] = ParkingSpot.objects.filter(spot_type='handicap').count()
    ctx['parkingspot_total_rate_per_hour'] = ParkingSpot.objects.aggregate(t=Sum('rate_per_hour'))['t'] or 0
    ctx['parkingbooking_count'] = ParkingBooking.objects.count()
    ctx['parkingbooking_active'] = ParkingBooking.objects.filter(status='active').count()
    ctx['parkingbooking_completed'] = ParkingBooking.objects.filter(status='completed').count()
    ctx['parkingbooking_cancelled'] = ParkingBooking.objects.filter(status='cancelled').count()
    ctx['parkingbooking_total_duration_hours'] = ParkingBooking.objects.aggregate(t=Sum('duration_hours'))['t'] or 0
    ctx['parkingvehicle_count'] = ParkingVehicle.objects.count()
    ctx['parkingvehicle_car'] = ParkingVehicle.objects.filter(vehicle_type='car').count()
    ctx['parkingvehicle_bike'] = ParkingVehicle.objects.filter(vehicle_type='bike').count()
    ctx['parkingvehicle_truck'] = ParkingVehicle.objects.filter(vehicle_type='truck').count()
    ctx['parkingvehicle_total_total_spent'] = ParkingVehicle.objects.aggregate(t=Sum('total_spent'))['t'] or 0
    ctx['recent'] = ParkingSpot.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def parkingspot_list(request):
    qs = ParkingSpot.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(spot_id__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(spot_type=status_filter)
    return render(request, 'parkingspot_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def parkingspot_create(request):
    if request.method == 'POST':
        obj = ParkingSpot()
        obj.spot_id = request.POST.get('spot_id', '')
        obj.zone = request.POST.get('zone', '')
        obj.spot_type = request.POST.get('spot_type', '')
        obj.floor = request.POST.get('floor', '')
        obj.rate_per_hour = request.POST.get('rate_per_hour') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/parkingspots/')
    return render(request, 'parkingspot_form.html', {'editing': False})


@login_required
def parkingspot_edit(request, pk):
    obj = get_object_or_404(ParkingSpot, pk=pk)
    if request.method == 'POST':
        obj.spot_id = request.POST.get('spot_id', '')
        obj.zone = request.POST.get('zone', '')
        obj.spot_type = request.POST.get('spot_type', '')
        obj.floor = request.POST.get('floor', '')
        obj.rate_per_hour = request.POST.get('rate_per_hour') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/parkingspots/')
    return render(request, 'parkingspot_form.html', {'record': obj, 'editing': True})


@login_required
def parkingspot_delete(request, pk):
    obj = get_object_or_404(ParkingSpot, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/parkingspots/')


@login_required
def parkingbooking_list(request):
    qs = ParkingBooking.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(spot_id__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'parkingbooking_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def parkingbooking_create(request):
    if request.method == 'POST':
        obj = ParkingBooking()
        obj.spot_id = request.POST.get('spot_id', '')
        obj.vehicle_number = request.POST.get('vehicle_number', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.driver_phone = request.POST.get('driver_phone', '')
        obj.entry_time = request.POST.get('entry_time') or None
        obj.exit_time = request.POST.get('exit_time') or None
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.amount = request.POST.get('amount') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/parkingbookings/')
    return render(request, 'parkingbooking_form.html', {'editing': False})


@login_required
def parkingbooking_edit(request, pk):
    obj = get_object_or_404(ParkingBooking, pk=pk)
    if request.method == 'POST':
        obj.spot_id = request.POST.get('spot_id', '')
        obj.vehicle_number = request.POST.get('vehicle_number', '')
        obj.driver_name = request.POST.get('driver_name', '')
        obj.driver_phone = request.POST.get('driver_phone', '')
        obj.entry_time = request.POST.get('entry_time') or None
        obj.exit_time = request.POST.get('exit_time') or None
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.amount = request.POST.get('amount') or 0
        obj.status = request.POST.get('status', '')
        obj.save()
        return redirect('/parkingbookings/')
    return render(request, 'parkingbooking_form.html', {'record': obj, 'editing': True})


@login_required
def parkingbooking_delete(request, pk):
    obj = get_object_or_404(ParkingBooking, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/parkingbookings/')


@login_required
def parkingvehicle_list(request):
    qs = ParkingVehicle.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(vehicle_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(vehicle_type=status_filter)
    return render(request, 'parkingvehicle_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def parkingvehicle_create(request):
    if request.method == 'POST':
        obj = ParkingVehicle()
        obj.vehicle_number = request.POST.get('vehicle_number', '')
        obj.owner_name = request.POST.get('owner_name', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.phone = request.POST.get('phone', '')
        obj.visits = request.POST.get('visits') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.pass_type = request.POST.get('pass_type', '')
        obj.pass_expiry = request.POST.get('pass_expiry') or None
        obj.save()
        return redirect('/parkingvehicles/')
    return render(request, 'parkingvehicle_form.html', {'editing': False})


@login_required
def parkingvehicle_edit(request, pk):
    obj = get_object_or_404(ParkingVehicle, pk=pk)
    if request.method == 'POST':
        obj.vehicle_number = request.POST.get('vehicle_number', '')
        obj.owner_name = request.POST.get('owner_name', '')
        obj.vehicle_type = request.POST.get('vehicle_type', '')
        obj.phone = request.POST.get('phone', '')
        obj.visits = request.POST.get('visits') or 0
        obj.total_spent = request.POST.get('total_spent') or 0
        obj.pass_type = request.POST.get('pass_type', '')
        obj.pass_expiry = request.POST.get('pass_expiry') or None
        obj.save()
        return redirect('/parkingvehicles/')
    return render(request, 'parkingvehicle_form.html', {'record': obj, 'editing': True})


@login_required
def parkingvehicle_delete(request, pk):
    obj = get_object_or_404(ParkingVehicle, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/parkingvehicles/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['parkingspot_count'] = ParkingSpot.objects.count()
    data['parkingbooking_count'] = ParkingBooking.objects.count()
    data['parkingvehicle_count'] = ParkingVehicle.objects.count()
    return JsonResponse(data)
