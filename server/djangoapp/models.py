from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """
    Stores information about a car manufacturer.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")

    # Optional additional field
    country = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"


class CarModel(models.Model):
    """
    Stores information about an individual car model.
    """

    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("COUPE", "Coupe"),
        ("CONVERTIBLE", "Convertible"),
        ("PICKUP", "Pickup"),
        ("VAN", "Van"),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="car_models"
    )

    dealer_id = models.IntegerField(
        help_text="ID of the dealer stored in the Cloudant database"
    )

    name = models.CharField(max_length=100)

    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default="SUV"
    )

    year = models.IntegerField(
        default=2023,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2026),
        ]
    )

    # Optional additional field
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name}"

    class Meta:
        ordering = ["car_make__name", "name", "-year"]
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"