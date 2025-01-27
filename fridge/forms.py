from django import forms
from .models import ItemType

class AddToInventoryForm(forms.Form):
    item_type = forms.ChoiceField(choices=[])
    expiration_date = forms.DateField(widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the dropdown with item types
        item_types = ItemType.objects.all()
        self.fields['item_type'].choices = [(item.barcode, item.name) for item in item_types]
