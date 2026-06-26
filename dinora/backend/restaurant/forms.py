from django import forms
from foodapp.models import FoodItem,Restaurant

class FoodForm(forms.ModelForm):

    class Meta:
        model = FoodItem

        fields = [
            
            'category',
            'name',
            'description',
            'price',
            'image'
        ]
class RestaurantProfileForm(forms.ModelForm):

    class Meta:
        model = Restaurant

        fields = [
            'name',
            'image',
            'description',
            'address',
            'phone',
            'email',
            'opening_time',
            'closing_time',
        ]        