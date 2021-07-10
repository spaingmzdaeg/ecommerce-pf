from django.db import models
from django.db.models.fields.files import ImageField
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email =  models.EmailField()
    profile_pic = ImageField(null=True, blank=True, upload_to='profile_pics')

    #META CLASS
    class Meta:
        db_table = 'customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'

    #TO STRING METHOD
    def __str__(self):
        return self.first_name + "-" + self.last_name

    #CLEAN METHOD
    # Run before savign the model
    '''def clean(self):
        pass'''

    #SAVE METHOD
    #ABSOLUTE URL METHOD
    '''def get_absolute_url(self):
        return reverse('customer_details', args=[str(self.customer_id)])
        #return reverse('customer_details', kwargs={'pk': self.customer_id})'''
    #OTHER METHODS
      
            

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    #price = models.DecimalField(max_digits=7, decimal_places=2)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    #image = ResizedImageField(size=[360,640],null=True,blank=True, upload_to='product_pics')
    image = models.ImageField(null=True, blank=True, upload_to='product_pics', default="default/placeholder.png")
    slug = models.SlugField(max_length=100, unique=True, blank=True)


    #META CLASS
    class Meta:
        db_table = 'product'
        verbose_name = 'product'
        verbose_name_plural = 'products'

    #TO STRING METHOD
    def __str__(self):
        return self.name

    #CLEAN METHOD   

    #SAVE METHOD
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    # ABSOLUTE URL METHOD
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.product_id)])
        #return reverse('product_details', kwargs={'pk': self.product_id})
    #OTHER METHODS
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''    
        return url
    '''
    sin default
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url   '''      

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, blank=True)

    #META CLASS
    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    #TO STRING METHOD
    def __str__(self):
        return str(self.order_id) + "-" + str(self.customer)

    #SAVE METHOD
    # ABSOLUTE URL METHOD
    '''def get_absolute_url(self):
        #return reverse('order_details', kwargs={'pk': self.order_id})
        return reverse('order_details', args=[str(self.order_id)])'''
    #OTHER METHODS
    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if i.product.digital == False:
                shipping = True
        return shipping
           
    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        #order_items = OrderItem.objects.all().select_related('order')
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        #order_items = OrderItem.objects.select_related('order').all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItem(models.Model):
    orderitem_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #META CLASS
    class Meta:
        db_table = 'orderitem'
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'

    #TO STRING METHOD
    def __str__(self):
        return str(self.orderitem_id)

    #SAVE METHOD
    # ABSOLUTE METHOD
    '''def get_absolute_url(self):
        #return reverse('orderitem_details', kwargs={'pk': self.orderitem_id})
        return reverse('order_item_details', args=[str(self.orderitem_id)])'''
    #OTHER METHODS
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total        

class ShippingAddress(models.Model):
    shippingaddress_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    #META CLASS
    class Meta:
        db_table = 'shippingaddress'
        verbose_name = 'shippingaddress'
        verbose_name_plural = 'shippingaddresses'

    #TO STRING METHOD
    def __str__(self):
        return str(self.address)

    #SAVE METHOD
    #GET URL ABSOLUT METHOD
    '''def get_absolute_url(self):
        #return reverse('shippingaddress_details', kwargs={'pk': self.shippingaddress_id})
        return reverse('shipping_address_details', args=[str(self.shippingaddress_id)])'''
    #OTHER METHODS