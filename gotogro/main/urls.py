# Define URL endpoints
# The places which the client can browse to

from django.urls import path
from . import views

app_name = "main"

# Endpoints
urlpatterns = [
    path("", views.home, name="home"),
    path("user-login", views.user_login, name="user_login"),
    path("user-logout", views.user_logout, name="user_logout"),
    path("members", views.members, name="members"),
    path("get-members", views.get_members, name="get_members"),
    path("items", views.items, name="items"),
    path("get-items", views.get_items, name="get_items"),
    path("sales", views.sales, name="sales"),
    path("salescsv",views.salescsv, name="salescsv"),
    path("memberscsv",views.memberscsv, name="memberscsv")
]