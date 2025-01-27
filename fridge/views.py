from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import IndividualItem, ItemType, ShoppingList
from .forms import AddToInventoryForm


def get_json_data(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


@csrf_exempt
@require_http_methods(["PUT"])
def add_item(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        item_type = ItemType.objects.get(unique_barcode=data['itemType'])
        IndividualItem.objects.create(
            type=item_type,
            expiration_date=data['expirationDate'],
            amount=data['amount']
        )
        return JsonResponse({"message": "Item added successfully"}, status=200)
    except ItemType.DoesNotExist:
        return JsonResponse({"error": "Item type not found"}, status=404)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_item(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        item = IndividualItem.objects.get(id=data['ID'])
        item.delete()
        return JsonResponse({"message": "Item removed successfully"}, status=200)
    except IndividualItem.DoesNotExist:
        return JsonResponse({"error": "Item not found"}, status=404)
    except KeyError:
        return JsonResponse({"error": "Missing ID field"}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_items(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        ids = [item['ID'] for item in data]
        deleted_count, _ = IndividualItem.objects.filter(id__in=ids).delete()
        return JsonResponse({"message": f"{deleted_count} items removed successfully"}, status=200)
    except KeyError:
        return JsonResponse({"error": "Invalid data format"}, status=400)


@csrf_exempt
@require_http_methods(["PUT"])
def new_type(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    try:
        ItemType.objects.create(
            unique_barcode=data['unique barcode'],
            name=data['name'],
            amount_type_id=data['amount type']
        )
        return JsonResponse({"message": "Item type added successfully"}, status=200)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_type(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    try:
        item_type = ItemType.objects.get(unique_barcode=data['unique barcode'])
        if IndividualItem.objects.filter(type=item_type).exists():
            return JsonResponse({"error": "Cannot delete, items of this type exist"}, status=400)
        item_type.delete()
        return JsonResponse({"message": "Item type removed successfully"}, status=200)
    except ItemType.DoesNotExist:
        return JsonResponse({"error": "Item type not found"}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def add_to_shopping_list(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    try:
        item_type = ItemType.objects.get(unique_barcode=data['item type'])
        shopping_item, created = ShoppingList.objects.get_or_create(item_type=item_type)
        shopping_item.amount += data['amount']
        shopping_item.save()
        return JsonResponse({"message": "Shopping list updated successfully"}, status=200)
    except ItemType.DoesNotExist:
        return JsonResponse({"error": "Item type not found"}, status=404)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_from_shopping_list(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    try:
        shopping_item = ShoppingList.objects.get(item_type_id=data['itemType'])
        shopping_item.amount -= data['amount']
        if shopping_item.amount <= 0:
            shopping_item.delete()
        else:
            shopping_item.save()
        return JsonResponse({"message": "Shopping list updated successfully"}, status=200)
    except ShoppingList.DoesNotExist:
        return JsonResponse({"error": "Item not found in shopping list"}, status=404)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)


@csrf_exempt
@require_http_methods(["PATCH"])
def purchase_item(request):
    data = get_json_data(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    try:
        shopping_item = ShoppingList.objects.get(item_type_id=data['item type'])
        IndividualItem.objects.create(
            type=shopping_item.item_type,
            expiration_date=data['expiration date'],
            amount=data['amount']
        )
        shopping_item.amount -= data['amount']
        if shopping_item.amount <= 0:
            shopping_item.delete()
        else:
            shopping_item.save()
        return JsonResponse({"message": "Item purchased and added to fridge"}, status=200)
    except ShoppingList.DoesNotExist:
        return JsonResponse({"error": "Item not found in shopping list"}, status=404)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)



def add_to_inventory(request):
    if request.method == 'POST':
        form = AddToInventoryForm(request.POST)
        if form.is_valid():
            # Process the form data and add to inventory
            item_type = form.cleaned_data['item_type']
            expiration_date = form.cleaned_data['expiration_date']
            # Handle saving the item to the inventory
            # Example:
            # InventoryItem.objects.create(item_type=item_type, expiration_date=expiration_date)
            return HttpResponse("Item added to inventory successfully.")
    else:
        form = AddToInventoryForm()

    return render(request, 'fridge/add_to_inventory.html', {'form': form})
