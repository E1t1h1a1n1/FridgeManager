from django import forms
from .models import ItemType

class AddToInventoryForm(forms.Form):
    item_type = forms.ChoiceField(choices=[])
    expiration_date = forms.DateField(widget=forms.SelectDateWidget)
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        item_types = ItemType.objects.all()
        self.fields['item_type'].choices = [(item.unique_barcode, item.name) for item in item_types]
