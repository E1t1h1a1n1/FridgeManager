from django.contrib import admin
from .models import AmountType, ItemType, IndividualItem, ShoppingList

admin.site.register(AmountType)
admin.site.register(ItemType)
admin.site.register(IndividualItem)
admin.site.register(ShoppingList)