"""Module is for defining inventory app models"""

import uuid

from django.db import models


class SeasonalEvents(models.Model):
    """SeasonalEvents model"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100, unique=True)


class Product(models.Model):
    """Product model"""

    IN_STOCK = "IS"
    OUT_OF_STOCK = "OOS"
    BACKORDERED = "BO"
    # defined the options above(and how the database will store them) and the
    # actual dictionary we will show on the dropdown whenever a new user is
    # created
    STOCK_STATUS = {
        IN_STOCK: "In Stock",
        OUT_OF_STOCK: "Out of Stock",
        BACKORDERED: "Back Ordered",
    }
    # max_lenght: Helps alocate the correct size of data,
    # optimize storage space
    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True)
    # description's not a mandatory field cause null=True
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    # When was the object created, we can only
    # take that date&time when using _add
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    # When was the object last updated, this one will take the date&time
    # when any change is made on the object
    is_active = models.BooleanField(default=False)
    stock_status = models.CharField(
        max_length=3,
        choices=STOCK_STATUS,
        default=OUT_OF_STOCK,
    )
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    seasonal_event = models.ForeignKey(SeasonalEvents, on_delete=models.CASCADE)
    #  you can use "" to avoid python herarchy, since I've defined
    #  SeasonalEvents before the Product model I can use it w/o ""


class ProductLine(models.Model):
    """ProductLine model"""

    # Recommended to use Decimal field instead of float,
    # precise number instead of approximations and such
    price = models.DecimalField()
    # by default null is already defined as False, price is a mandatory field
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductImage(models.Model):
    """ProductImage model"""

    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField()
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)


class Category(models.Model):
    """Category model"""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=False)
