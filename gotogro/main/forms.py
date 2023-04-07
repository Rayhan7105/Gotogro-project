# Define forms
# The client"s way of submitting data to server

from django import forms
from .models import Member, Item, Sale

class MemberForm(forms.ModelForm):
    # Fields
    first_name = forms.CharField(widget=forms.TextInput(attrs={"data-default-value": "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"data-default-value": "Last name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'data-default-value': 'Email'}))
    postcode = forms.CharField(max_length=4, min_length=4, widget=forms.TextInput(attrs={'data-default-value': 'Postcode'}))

    # Model
    class Meta:
        model = Member
        fields = ("first_name", "last_name", "email", "postcode")

class ItemForm(forms.ModelForm):
    # Fields
    name = forms.CharField(widget=forms.TextInput(attrs={"data-default-value": "Name"}))
    price = forms.FloatField(widget=forms.TextInput(attrs={"data-default-value": "Price"}))
    stock = forms.IntegerField(widget=forms.TextInput(attrs={"data-default-value": "Stock"}))

    # Model
    class Meta:
        model = Item
        fields = "__all__"

class SaleForm(forms.ModelForm):
    # Fields
    member = forms.ModelChoiceField(queryset=Member.objects.all())
    item = forms.ModelMultipleChoiceField(queryset=Item.objects.filter(stock__gt=0))
    total = forms.FloatField(widget=forms.TextInput(attrs={"data-default-value": "Total"}))

    # Model
    class Meta:
        model = Sale
        fields =("member", "item", "total")