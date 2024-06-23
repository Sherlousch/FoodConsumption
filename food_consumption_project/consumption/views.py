from django.shortcuts import render
from consumption.models import Consumer, Consumption, FoodType
from django.http import JsonResponse, Http404

# Create your views here.
def consumption_view(request):
    consumers = Consumer.objects.all()
    consumers_data = [ {"id": consumer.pk , "name": consumer.name} for consumer in consumers]
    consumption_data = get_data(consumer_id=consumers[0].pk)
    food_type_data = get_food_types()
    context = {
        "consumers": consumers_data,
        "food_types": food_type_data,
        "data": consumption_data,
        "titles": {
            "sankey": "Food consumption per year (kg) and food/feed destination",
            "water": "Freshwater withdrawal (L)",
            "land": "Land use (m2)",
            "gas": "CO2 emissions (kg)"
        },
        "extra_colors": {
            "Food": "#CCA290",
            "Feed": "#BDA79E"
        }
    }
    return render(request, "dashboard.html", context=context)

def data_view(request, consumer_id):
    data = get_data(consumer_id)
    if not data:
        raise Http404("Consumer does not exist")
    return JsonResponse(get_data(consumer_id))

def get_data(consumer_id):
    consumer = Consumer.objects.filter(pk=consumer_id)
    if not consumer:
        return None
    consumptions = Consumption.objects.filter(consumer=consumer_id)
    data = {}
    for consumption in consumptions:
        data[consumption.food_type.name] = {
            "food": consumption.food_consumption,
            "feed": consumption.feed_consumption
        }
    return data

def get_food_types():
    food_types = FoodType.objects.all()
    data = {}
    for food_type in food_types:
        data[food_type.name] = {
            "color": food_type.color[:7], 
            "water": food_type.freshwater_withdrawal_l,
            "land": food_type.land_use_m2,
            "gas": food_type.gas_emission_kg_co2
        }
    return data