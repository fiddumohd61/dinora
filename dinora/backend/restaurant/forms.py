from django import forms
from foodapp.models import FoodItem

class FoodForm(forms.ModelForm):

    class Meta:
        model = FoodItem

        fields = [
            'restaurant',
            'category',
            'name',
            'description',
            'price',
            'image'
        ]