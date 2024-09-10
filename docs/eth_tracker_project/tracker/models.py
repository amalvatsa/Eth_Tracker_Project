from django.db import models

class Deposit(models.Model):
    block_number = models.BigIntegerField()
    tx_hash = models.CharField(max_length=66, unique=True)
    sender = models.CharField(max_length=42)
    amount = models.DecimalField(max_digits=20, decimal_places=18)
    fee = models.DecimalField(max_digits=20, decimal_places=18)
    pubkey = models.CharField(max_length=98, blank=True, null=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Deposit {self.tx_hash} from {self.sender}"