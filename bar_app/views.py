from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Beer, NyamaChoma, Category, Table, Reservation
from accommodation.models import Room, RoomType
from .forms import ReservationForm

def home(request):
    # Get featured items, handle case where no items exist yet
    featured_beers = Beer.objects.filter(in_stock=True)[:6]
    featured_nyama = NyamaChoma.objects.filter(available=True)[:4]
    available_rooms = Room.objects.filter(is_available=True)[:3]
    
    context = {
        'featured_beers': featured_beers,
        'featured_nyama': featured_nyama,
        'available_rooms': available_rooms,
    }
    return render(request, 'bar_app/home.html', context)

def beer_menu(request):
    category_filter = request.GET.get('category')
    beer_type_filter = request.GET.get('type')
    
    beers = Beer.objects.filter(in_stock=True)
    
    if category_filter:
        beers = beers.filter(category__name=category_filter)
    if beer_type_filter:
        beers = beers.filter(beer_type=beer_type_filter)
    
    categories = Category.objects.all()
    beer_types = Beer.BEER_TYPES
    
    paginator = Paginator(beers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'beer_types': beer_types,
        'current_category': category_filter,
        'current_type': beer_type_filter,
    }
    return render(request, 'bar_app/beer_menu.html', context)

def nyama_choma_menu(request):
    meat_type_filter = request.GET.get('meat_type')
    
    nyama_items = NyamaChoma.objects.filter(available=True)
    
    if meat_type_filter:
        nyama_items = nyama_items.filter(meat_type=meat_type_filter)
    
    meat_types = NyamaChoma.MEAT_TYPES
    
    context = {
        'nyama_items': nyama_items,
        'meat_types': meat_types,
        'current_meat_type': meat_type_filter,
    }
    return render(request, 'bar_app/nyama_menu.html', context)

def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return JsonResponse({'success': True, 'message': 'Reservation made successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReservationForm()
        available_tables = Table.objects.filter(is_reserved=False)
    
    context = {
        'form': form,
        'available_tables': available_tables,
    }
    return render(request, 'bar_app/reservation.html', context)
