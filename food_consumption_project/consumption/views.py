from django.shortcuts import render
from consumption.models import Consumer, Consumption
from django.http import JsonResponse, Http404

# Create your views here.
def consumption_view(request):
    consumers = Consumer.objects.all()
    consumers_data = [ {"id": consumer.pk , "name": consumer.name} for consumer in consumers]
    consumption_data = get_data(consumer_id=consumers[0].pk)
    context = {
        "consumers": consumers_data,
        "data": consumption_data
    }
    return render(request, "dashboard.html", context=context)

def data_view(request, consumer_id):
    return JsonResponse(get_data(consumer_id))


def get_data(consumer_id):
    consumer = Consumer.objects.filter(pk=consumer_id)
    if not consumer:
        raise Http404("Consumer does not exist")
    consumption_list = Consumption.objects.filter(consumer=consumer_id)
    consumption_data = {
        "title": f"{consumer[0].name} food consumption per year (kg) and food/feed destination",
        "data": []
        }
    water_data = {
        "title": "Freshwater withdrawal (L)",
        "data": []
        }
    land_data = {
        "title": "Land use (m2)",
        "data": []
        }
    co2_data = {
        "title": "CO2 emissions (kg)",
        "data": []
        }
    colors = {
        "Food": "#CCA290",
        "Feed": "#BDA79E"
    }
    for consumption in consumption_list:
        consumption_data["data"].append({"from": consumption.food_type.name, "to": "Food", "weight": consumption.food_consumption})
        consumption_data["data"].append({"from": consumption.food_type.name, "to": "Feed", "weight": consumption.feed_consumption})
        water_data["data"].append({
            "label": consumption.food_type.name,
            "data": [ 
                ["Food", consumption.food_type.freshwater_withdrawal_l * consumption.food_consumption],
                ["Feed", consumption.food_type.freshwater_withdrawal_l * consumption.feed_consumption]
                ]
            })
        land_data["data"].append({
            "label": consumption.food_type.name,
            "data": [ 
                ["Food", consumption.food_type.land_use_m2 * consumption.food_consumption],
                ["Feed", consumption.food_type.land_use_m2 * consumption.feed_consumption]
                ]
            })
        co2_data["data"].append({
            "label": consumption.food_type.name,
            "data": [ 
                ["Food", consumption.food_type.gas_emission_kg_co2 * consumption.food_consumption],
                ["Feed", consumption.food_type.gas_emission_kg_co2 * consumption.feed_consumption]
                ]
            })
        colors[consumption.food_type.name] = consumption.food_type.color[:7] # Remove alpha factor of colors
    data = {
        "consumption": consumption_data,
        "water": water_data,
        "land": land_data,
        "co2": co2_data,
        "colors": colors
    }
    return data

