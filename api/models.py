from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Product(models.Model):
    """
    This model is a template for representation of the purchases
    """

    name = models.CharField(max_length=50)
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
    )
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name + f"with the cost {self.cost}"


class SalePoint(models.Model):
    """
    representation of the shop
    """

    address = models.CharField(max_length=70, unique=True)
    description = models.TextField(blank=True)
    administrators = models.ManyToManyField(
        "SalePointAdministrator", related_name="sale_points"
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # to identify the shop through the user

    def get_absolute_url(self):
        pass

    def calculate_purchases_sum(self, **kwargs):
        pass

    def get_administrators(self):
        pass

    def __str__(self):
        return f"Sale point with the address: {self.address}"


class Purchase(models.Model):
    """
    the main source of functionality for this project
    """

    sale_point = models.ForeignKey(
        "SalePoint", on_delete=models.CASCADE, related_name="purchases"
    )
    product = models.OneToOneField("Product", on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        pass

    def calculate_total(self):
        return self.count * self.product.cost


class SalePointAdministrator(models.Model):
    """
    hidden fields:
    - sale_points - points to the SalePoint ManyToMany relation
    """

    full_name = models.CharField(max_length=100, unique=True)
    experience = models.DurationField(default=timedelta(0))
    is_main_administrator = models.BooleanField(default=False)

    def __str__(self):
        return (
            self.full_name
            + f"{'is' if self.is_main_administrator else 'is not'} the main administrator"
        )
