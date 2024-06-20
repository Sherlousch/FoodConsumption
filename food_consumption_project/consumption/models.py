from django.db import models

class FoodType(models.Model):
    name = models.CharField("Name", max_length=240)
    gas_emission_kg_co2 = models.FloatField("Gas emission in kg CO2")
    freshwater_withdrawal_l = models.FloatField("Freshwater withdrawal in L")
    land_use_m2 = models.FloatField("Land use in m2")
    class FoodType(models.TextChoices):
        MEAT = "MEAT", "Meat"
        FISH = "FISH", "Fish"
        VEGGIE = "VEGGIE", "Veggie"
        VEGAN = "VEGAN", "Vegan"

    def __str__(self) -> str:
        return self.name

class Consumer(models.Model):
    name = models.CharField("Name", max_length=240)

    def __str__(self) -> str:
        return self.name

class Consumption(models.Model):
    consumer = models.ForeignKey(
        "consumption.Consumer", verbose_name="consumer", on_delete=models.CASCADE, related_name="consumption_set"
        )
    
    food_type = models.ForeignKey(
        "consumption.FoodType", verbose_name="food type", on_delete=models.CASCADE
        )
    
    food_consumption = models.FloatField("kg consumed for human food")
    feed_consumption = models.FloatField("kg consumed for animal feed")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['consumer', 'food_type'], name='unique_consumer_food_type_combination'
            )
        ]

    def __str__(self) -> str:
        return f"{self.consumer} {self.food_type} consumption : Food {self.food_consumption} kg, Feed {self.feed_consumption} kg per year"


