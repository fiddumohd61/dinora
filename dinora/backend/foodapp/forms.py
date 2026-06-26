from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = ["rating", "review"]

        widgets = {
            "rating": forms.Select(
                choices=[
                    (1, "⭐ 1"),
                    (2, "⭐⭐ 2"),
                    (3, "⭐⭐⭐ 3"),
                    (4, "⭐⭐⭐⭐ 4"),
                    (5, "⭐⭐⭐⭐⭐ 5"),
                ]
            ),
            "review": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Share your experience...",
                    "class": "form-control",
                }
            ),
        }
