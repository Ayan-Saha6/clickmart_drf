from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product



User=get_user_model()


class Order(models.Model):

    STATUS_CHOICES=[
        ('PENDING','pending'),
        ('CONFIRMED','confirmed'),              # this is basically the value and lebel pair
        ('DELIVERED','delivered')
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    tax_amount= models.DecimalField(max_digits=10 , decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20,choices= STATUS_CHOICES,default='PENDING')
    address= models.CharField(max_length=200,blank=True,null=True)
    phone=models.CharField(max_length=15,blank=True,null=True)
    city=models.CharField(max_length=25,blank=True,null=True)
    state=models.CharField(max_length=25,blank=True,null=True)
    zip_code=models.CharField(max_length=10,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


class OrderItem(models.Model):   #in one order we can have multiple item, so we need OrderItem model
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete= models.PROTECT) #even if the product is deleted orderitem will not be deleted
    quantity= models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)  #its single product price
    total_price= models.DecimalField(max_digits=10,decimal_places=2) # price * quantitry

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    