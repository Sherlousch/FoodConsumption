from django.shortcuts import render
from consumption.models import Consumer, Consumption
from django.http import JsonResponse, Http404

# Create your views here.
def consumption_view(request):
    consumers = Consumer.objects.all
    consumption_data = get_data(request, consumer=consumers[0].pk)


def get_data(request, consumer_id):
    consumer = Consumer.objects.filter(pk=consumer_id)
    if not consumer:
        raise Http404("Consumer does not exist")
    consumption_list = Consumption.objects.filter(consumer=consumer_id)
    consumption_data = {
        "title": f"{consumer[0].name} food consumption per year (kg) and food/feed destination",
        "data": [],
        "labels": []
        }
    water_data = {
        "title": "Freshwater withdrawal (L)",
        "data": [],
        "labels": []
        }
    land_data = {
        "title": "Land use (m2)",
        "data": [],
        "labels": []
        }
    co2_data = {
        "title": "CO2 emissions (kg)",
        "data": [],
        "labels": []
        }
    for consumption in consumption_list:
        consumption_data["data"].append({"from": consumption.food_type.name, "to": "Food", "weight": consumption.food_consumption})
        consumption_data["data"].append({"from": consumption.food_type.name, "to": "Feed", "weight": consumption.feed_consumption})
        water_data["data"].append([ 
            ["Food", consumption.food_type.freshwater_withdrawal_l * consumption.food_consumption],
            ["Feed", consumption.food_type.freshwater_withdrawal_l * consumption.feed_consumption]
            ])
        water_data["labels"].append(consumption.food_type.name)
        land_data["data"].append([ 
            ["Food", consumption.food_type.land_use_m2 * consumption.food_consumption],
            ["Feed", consumption.food_type.land_use_m2 * consumption.feed_consumption]
            ])
        land_data["labels"].append(consumption.food_type.name)
        co2_data["data"].append([ 
            ["Food", consumption.food_type.gas_emission_kg_co2 * consumption.food_consumption],
            ["Feed", consumption.food_type.gas_emission_kg_co2 * consumption.feed_consumption]
            ])
        co2_data["labels"].append(consumption.food_type.name)
    data = {
        "consumption_data": consumption_data,
        "water_data": water_data,
        "land_data": land_data,
        "co2_data": co2_data
    }
    return JsonResponse({'data': data})