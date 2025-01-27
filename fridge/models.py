from django.db import models

class AmountType(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class ItemType(models.Model):
    unique_barcode = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    amount_type = models.ForeignKey(AmountType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IndividualItem(models.Model):
    id = models.AutoField(primary_key=True)
    expiration_date = models.DateField()
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.type.name} - {self.expiration_date}"


class ShoppingList(models.Model):
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    amount = models.FloatField()

    class Meta:
        unique_together = ('item_type', 'amount')  # Composite primary key

    def __str__(self):
        return f"Shopping List Item: {self.item_type.name} - Amount: {self.amount}"