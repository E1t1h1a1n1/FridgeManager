from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/addItem', views.add_item, name='add_item'),
    path('api/v1/removeItem', views.remove_item, name='remove_item'),
    path('api/v1/removeItems', views.remove_items, name='remove_items'),
    path('api/v1/newType', views.new_type, name='new_type'),
    path('api/v1/removeType', views.remove_type, name='remove_type'),
    path('api/v1/addToShoppingList', views.add_to_shopping_list, name='add_to_shopping_list'),
    path('api/v1/removeFromShoppingList', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('api/v1/purchaseItem', views.purchase_item, name='purchase_item'),
    path('addToInventory', views.add_to_inventory, name='add_to_inventory'),
]
