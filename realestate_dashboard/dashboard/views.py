# views.py in your Django app
from django.shortcuts import render
from .models import SaleDataset
from django.db.models import Avg, Count, Max, Sum
from collections import defaultdict
from django.core.serializers.json import DjangoJSONEncoder
import json


def zagreb_sale_data(request):
    # Query SaleDataset for Zagreb data
    datasets = SaleDataset.objects.filter(city__name="Zagreb").values(
        'calendar_week', 'calendar_year'
    ).annotate(
        average_price=Avg('average_price'),
        average_price_per_sqm=Avg('average_price_per_sqm'),
        total_raw=Sum('total_raw'),
        total_clean_entries=Sum('total_clean_entries'),
        highest_price=Max('highest_price')
    ).order_by('calendar_year', 'calendar_week')

    # Organize data by year
    data_by_year = defaultdict(lambda: defaultdict(list))
    for dataset in datasets:
        year = dataset['calendar_year']
        week = dataset['calendar_week']
        data_by_year['average_prices'][year].append((week, float(dataset['average_price'])))
        data_by_year['average_prices_sqm'][year].append((week, float(dataset['average_price_per_sqm'])))
        data_by_year['total_raw_data'][year].append((week, dataset['total_raw']))
        data_by_year['total_clean_entries'][year].append((week, dataset['total_clean_entries']))
        data_by_year['highest_prices'][year].append((week, float(dataset['highest_price'])))

    context = {
        'data_by_year_json': json.dumps(data_by_year, cls=DjangoJSONEncoder)
    }

    return render(request, 'zagreb_sale_data.html', context)


def rijeka_sale_data(request):
    # Query SaleDataset for Rijeka data
    datasets = SaleDataset.objects.filter(city__name="Rijeka").values(
        'calendar_week', 'calendar_year'
    ).annotate(
        average_price=Avg('average_price'),
        average_price_per_sqm=Avg('average_price_per_sqm'),
        total_raw=Avg('total_raw'),
        total_clean_entries=Avg('total_clean_entries')
    ).order_by('calendar_year', 'calendar_week')

    # Organize data by year
    data_by_year = {
        'average_price': {},
        'average_price_per_sqm': {},
        'total_raw': {},
        'total_clean_entries': {}
    }
    for dataset in datasets:
        year = dataset['calendar_year']
        week = dataset['calendar_week']
        for key in data_by_year:
            if year not in data_by_year[key]:
                data_by_year[key][year] = []
            data_by_year[key][year].append({
                'week': week, 
                'value': dataset[key]
            })

    context = {
        'data_by_year_json': json.dumps(data_by_year, cls=DjangoJSONEncoder)
    }

    return render(request, 'rijeka_sale_data.html', context)