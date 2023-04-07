# Define views
# The server"s response to client requests
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import MemberForm, ItemForm, SaleForm
from .models import Member, Item, Sale
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse


@login_required(login_url="/user-login", redirect_field_name=None)
def home(request):
    return render(request, "home.html", {})
    

def user_login(request):
    # If client sends POST request, create form from data
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)

        # If form is valid, authenticate
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            # If authentication succeded, complete login and display message
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {username}")
                return redirect("main:home")
            else:
                messages.error(request, f"Failed to login as {username}")
        else:
            messages.error(request, f"Invalid username or password")

    # If client sends GET request, return login page
    login_form = AuthenticationForm()
    return render(request, "login.html", {"login_form": login_form})


@login_required(login_url="/user-login", redirect_field_name=None)
def user_logout(request):  
    logout(request)
    messages.success(request, "Logged out")
    return redirect("main:user_login")

@login_required(login_url="/user-login", redirect_field_name=None)
def members(request):
    # If client sends POST request, create form from data
    if request.method == "POST":
        member_form = MemberForm(request.POST)

        # If form is valid, create member and display message
        if member_form.is_valid():
            first_name = member_form.cleaned_data.get("first_name")
            last_name = member_form.cleaned_data.get("last_name")
            member_form.save()
            messages.success(request, f"New member added: {first_name} {last_name}")
            return redirect("main:home")
        else:
            messages.error(request, f"Failed to add member")

    # Iterate over all sales
    sales = {}
    for sale in Sale.objects.all():
        # Add member to sales dict
        if not sale.member in sales:
            sales[sale.member] = {}

        # Store item frequency under member
        for item in sale.item.all():
            if not item in sales[sale.member]:
                sales[sale.member][item] = 0
            sales[sale.member][item] += 1

    # Extract most frequent item for each member
    for sale in sales.items():
        sales[sale[0]] = max(sale[1], key=sale[1].get)

    # If client sends GET request, return member page
    member_form = MemberForm()
    return render(request, "members.html", {"member_form": member_form, "members": Member.objects.all(), "sales": sales})



@login_required(login_url="/user-login", redirect_field_name=None)
def get_members(request):
    members = serializers.serialize("json", Member.objects.all())
    return JsonResponse({"members": members})


@login_required(login_url="/user-login", redirect_field_name=None)
def items(request):
    # If client sends POST request, create form from data
    if request.method == "POST":
        item_form = ItemForm(request.POST)

        # If form is valid, create member and display message
        if item_form.is_valid():
            name = item_form.cleaned_data.get("name")
            item_form.save()
            messages.success(request, f"New item added: {name}")
            return redirect("main:home")
        else:
            messages.error(request, f"Failed to add item")

    # If client sends GET request, return member page
    item_form = ItemForm()
    return render(request, "items.html", {"item_form": item_form, "items": Item.objects.filter(stock__gt=0)})


@login_required(login_url="/user-login", redirect_field_name=None)
def get_items(request):
    items = serializers.serialize("json", Item.objects.all())
    return JsonResponse({"items": items})


@login_required(login_url="/user-login", redirect_field_name=None)
def sales(request):
    # If client sends POST request, create form from data
    if request.method == "POST":
        sale_data = request.POST.copy()
        total = 0

        # Iterate over items and decrement stock by 1
        for id in sale_data["item"].split(","):
            item = Item.objects.get(id=id)
            item.stock -= 1
            item.save()
            total += item.price

        # Add sale total and create form
        sale_data["total"] = total
        sale_form = SaleForm(sale_data)

        # If form is valid, create member and display message
        if sale_form.is_valid():
            member = sale_form.cleaned_data.get("member")
            sale_form.save()
            messages.success(request, f"New sale added for: {member}")
            return redirect("main:home")
        else:
            messages.error(request, f"Failed to add sale")

    # If client sends GET request, return member page
    sale_form = SaleForm()
    return render(request, "sales.html", {"sale_form": sale_form, "sales": Sale.objects.all()})

# @login_required(login_url="/user-login", redirect_field_name=None)
def salescsv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="sales.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['member', 'item', 'total', 'date'])

    for sale in Sale.objects.all().values_list('member', 'item', 'total', 'date'):
        writer.writerow(sale)

    return response

def memberscsv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Cotent-Disposition': 'attachment; filename="members.csv"'}
    )

    writer = csv.writer(response)
    writer.writerow(['first_name','last_name','email','postcode', 'registration_date'])

    for member in Member.objects.all().values_list('first_name','last_name','email','postcode', 'registration_date'):
        writer.writerow(member)

    return response 
