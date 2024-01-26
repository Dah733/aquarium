import json
import datetime
from django.core.management.base import BaseCommand
from aquariumapp.models import Metric

class Command(BaseCommand):
    help = 'Add test data to the Metric model'

    def handle(self, *args, **kwargs):
        test_data = [
            {"water_temperature": 25.5, "air_temperature": 28.0, "water_filter_flow": 10.2, "pH": 7.0, "water_turbidity": 15.0, "light_intensity": 2500},
            {"water_temperature": 22.5, "air_temperature": 26.0, "water_filter_flow": 11.0, "pH": 6.0, "water_turbidity": 12.0, "light_intensity": 1500},
            {"water_temperature": 23.5, "air_temperature": 27.0, "water_filter_flow": 10.0, "pH": 5.0, "water_turbidity": 14.0, "light_intensity": 2000},
            {"water_temperature": 24.5, "air_temperature": 25.0, "water_filter_flow": 10.7, "pH": 6.0, "water_turbidity": 13.0, "light_intensity": 1300},
            {"water_temperature": 21.5, "air_temperature": 22.0, "water_filter_flow": 10.5, "pH": 7.0, "water_turbidity": 16.0, "light_intensity": 1500},
            {"water_temperature": 20.5, "air_temperature": 24.0, "water_filter_flow": 11.2, "pH": 8.0, "water_turbidity": 15.0, "light_intensity": 1200},
            {"water_temperature": 22.5, "air_temperature": 23.0, "water_filter_flow": 9.2, "pH": 5.0, "water_turbidity": 11.0, "light_intensity": 1400},
            {"water_temperature": 24.5, "air_temperature": 25.0, "water_filter_flow": 9.5, "pH": 6.0, "water_turbidity": 13.0, "light_intensity": 2100},
            {"water_temperature": 23.5, "air_temperature": 27.0, "water_filter_flow": 9.7, "pH": 7.0, "water_turbidity": 12.0, "light_intensity": 1600},
            {"water_temperature": 25.5, "air_temperature": 26.0, "water_filter_flow": 9.9, "pH": 8.0, "water_turbidity": 14.0, "light_intensity": 1800},
        ]

        for data in test_data:
            Metric.objects.create(
                water_temperature=data["water_temperature"],
                air_temperature=data["air_temperature"],
                water_filter_flow=data["water_filter_flow"],
                pH=data["pH"],
                water_turbidity=data["water_turbidity"],
                light_intensity=data["light_intensity"],
                timestamp=datetime.datetime.now()
            )

        self.stdout.write(self.style.SUCCESS('Test data added successfully'))
