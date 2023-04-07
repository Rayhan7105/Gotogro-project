# Register models in admin interface

from django.contrib import admin
from .models import Member, Item, Sale

admin.site.register(Member)
admin.site.register(Item)
admin.site.register(Sale)