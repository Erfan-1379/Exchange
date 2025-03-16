from djongo import models

class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.price}"
