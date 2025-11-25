from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Location(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin","Admin"),
        ("user", "User"),
        ("mechanic", "Mechanic"),
        ("fuels", "Fuels"),
    ]
    role = models.CharField(max_length=200, default="user")

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    name=models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    dob = models.DateField(null=True)
    profile_pic = models.ImageField(upload_to="userprofile",default='static/images/profile/default.jpg', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class MechanicProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mechanic_profile")
    name=models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="mechanic_location")
    phone = models.CharField(max_length=200)
    dob = models.DateField(null=True)
    skills = models.TextField()
    experience = models.CharField(max_length=200)
    STATUS_CHOICES = [
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")
    SPECIALIZATION_CHOICES = [
        ("two_wheeler", "Two Wheeler"),
        ("four_wheeler", "Four Wheeler"),
        ("heavy_vehicle", "Heavy Vehicle"),
    ]
    specialized_in = models.CharField(max_length=200, choices=SPECIALIZATION_CHOICES)
    bio = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to="mech_pics",default='static/images/profile/default.jpg', blank=True, null=True)

    def __str__(self):
        return self.user.username


class ReqToMechanic(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="req_profile")
    mechanic=models.ForeignKey(MechanicProfile,on_delete=models.CASCADE,related_name="req_profile")
    discription=models.CharField(max_length=200)
    phone=models.IntegerField()
    location=models.ForeignKey(Location,on_delete=models.CASCADE,related_name="req_location")
    latitude=models.FloatField(null=True)
    longtitude=models.FloatField(null=True)
    address=models.TextField(null=True)
    link=models.URLField(null=True)
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("Payment Pending", "Payment Pending"),
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")
    datetime=models.DateTimeField(auto_now_add=True,null=True)


class Bill(models.Model):
    customer=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    mechanic=models.ForeignKey(MechanicProfile,on_delete=models.CASCADE)
    req=models.ForeignKey(ReqToMechanic,on_delete=models.CASCADE)
    payment=models.PositiveBigIntegerField()
    platform_fee = models.PositiveIntegerField(null=True)
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("pending", "Pending"),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")
    
    def save(self, *args, **kwargs):
        # Calculate platform fee as 5% of the payment
        self.platform_fee = int(self.payment * 0.05)
        super().save(*args, **kwargs)


class UserPayment(models.Model):
    customer=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='cust_pay')
    mechanic=models.ForeignKey(MechanicProfile,on_delete=models.CASCADE,related_name='mech_pay')
    req=models.ForeignKey(ReqToMechanic,on_delete=models.CASCADE,related_name='user_pay')
    acholdername=models.CharField(max_length=100)
    accno=models.PositiveBigIntegerField()
    cvv=models.IntegerField()
    exp=models.CharField(max_length=100)
    amount=models.PositiveBigIntegerField()
    
    def __str__(self):
        return self.acholdername


class FeedBack(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="feedback_userprofile")
    request=models.ForeignKey(ReqToMechanic,on_delete=models.CASCADE,related_name="feedback_req",null=True)
    mechanic=models.ForeignKey(MechanicProfile,on_delete=models.CASCADE,related_name="feedback_mechanicprofile")
    text=models.TextField()
    options=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
    )
    rating=models.CharField(max_length=200,choices=options,default="5")
    date=models.DateTimeField(auto_now_add=True)

class Fuel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="fuel_owner")
    price = models.IntegerField()
    logo = models.FileField(upload_to="fuel_logo")
    fuel_dealer = models.CharField(max_length=100)   
    location = models.ForeignKey(Location, on_delete=models.CASCADE,default="1")

    options = (
        ('Petrol','Petrol'),
        ('Diesel','Diesel'),
    )
    fuel_type = models.CharField(max_length=100,choices=options)
    
    def __str__(self):
        return f"{self.fuel_dealer} - {self.fuel_type}"
    
    
class ReqFuel(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="req_fuel")
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, related_name="user_fuel")
    quantity = models.IntegerField(null=True)
    phone = models.IntegerField()
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    address = models.TextField(null=True)
    link = models.URLField(null=True)
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("Payment Pending", "Payment Pending"),
        ("pending", "Pending"),
        ("OrderConfirmed", "OrderConfirmed"),
        ("Out For Delivery", "Out For Delivery"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")
    datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.name} - {self.fuel.fuel_type} - {self.status}"


class BillFuel(models.Model):
    customer=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    fuel=models.ForeignKey(Fuel,on_delete=models.CASCADE)
    req=models.ForeignKey(ReqFuel,on_delete=models.CASCADE)
    payment=models.PositiveBigIntegerField()
    platform_fee = models.PositiveIntegerField(null=True)
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("pending", "Pending"),
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        # Calculate platform fee as 5% of the payment
        self.platform_fee = int(self.payment * 0.05)
        super().save(*args, **kwargs)


class UserPaymentFuel(models.Model):
    customer=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='cust_pay_fuel')
    fuel=models.ForeignKey(Fuel,on_delete=models.CASCADE,related_name='fuel_pay')
    req=models.ForeignKey(ReqFuel,on_delete=models.CASCADE,related_name='user_pay_fuel')
    acholdername=models.CharField(max_length=100)
    accno=models.PositiveBigIntegerField()
    cvv=models.IntegerField()
    exp=models.CharField(max_length=100)
    amount=models.PositiveBigIntegerField()
    
    def __str__(self):
        return self.acholdername


class FeedBackFuel(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="feedback_user")
    request=models.ForeignKey(ReqFuel,on_delete=models.CASCADE,related_name="feedback_fuel",null=True)
    fuel=models.ForeignKey(Fuel,on_delete=models.CASCADE,related_name="feedback_s")
    text=models.TextField()
    options=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
    )
    rating=models.CharField(max_length=200,choices=options,default="5")
    date=models.DateTimeField(auto_now_add=True)



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_item_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_item_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_item_total(self):
        return self.price * self.quantity
    
    
    
class OrderPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    account_holder_name = models.CharField(max_length=100)
    account_number = models.PositiveBigIntegerField()
    cvv = models.IntegerField()
    expiry_date = models.CharField(max_length=7)  # Format: MM/YYYY
    amount = models.PositiveBigIntegerField()
    
    def __str__(self):
        return f"Payment for Order #{self.order.id}"