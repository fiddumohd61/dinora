from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'email'
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email Address'
                }
            ),
        }