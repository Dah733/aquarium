from django import forms

class MetricSettingForm(forms.Form):
    water_temperature = forms.FloatField()
    air_temperature = forms.FloatField()
    water_filter_flow = forms.FloatField()
    pH = forms.FloatField()
    water_turbidity = forms.FloatField()
    light_intensity = forms.FloatField()
