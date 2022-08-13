from django import forms
from decimal import Decimal
from .models import categories

class CreateListing(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput)
    description = forms.CharField(label='Description',widget=forms.TextInput)
    Starting_bid = forms.DecimalField(label='Starting Bid', widget=forms.NumberInput, min_value=0.01, decimal_places=2)
    image_URL = forms.URLField(label='Image URL', required=False, empty_value="https://st4.depositphotos.com/14953852/22772/v/1600/depositphotos_227725020-stock-illustration-image-available-icon-flat-vector.jpg")

    list_category = categories.objects.all()
    form_categories = [(c, c) for c in list_category]
    category = forms.ChoiceField(label='Category', choices=form_categories)
