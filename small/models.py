from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# ������ ���������� ���������� � ������, � �������� �� ���������.
# ��� �������� ���� � ��������� ����� ������.
# ������ ���� ������ ������������ ���� ������� � ���� ������.
# ������ ������ ��� ����� �������������� �� django.db.models.Model.
# ������� ������ ������������ ���� � ���� ������.
# Django ������������� ������������� ��������� API ��� ������� � ������

# choices (������ ������). �������� (��������, ������ ��� ������) 2-� ���������� ��������,
# ������������ �������� �������� ��� ����.
# ��� �����������, ������ ����� ���������� select ������ ������������ ���������� ����
# � ��������� �������� ���� ���������� ����������.

# ��������� ������
class  Kind(models.Model):
    # ����������� ��� ���� (�����, label). ������ ����, ����� ForeignKey, ManyToManyField � OneToOneField,
    # ������ ���������� ��������� �������������� ����������� ��������.
    # ���� ��� �� �������, Django �������������� ������� ���, ��������� �������� ����, ������� ������������� �� ������.
    # null - ���� True, Django �������� ������ �������� ��� NULL � ���� ������. �� ��������� - False.
    # blank - ���� True, ���� �� ����������� � ����� ���� ������. �� ��������� - False.
    # ��� �� �� �� ��� � null. null ��������� � ���� ������, blank - � �������� ������.
    # ���� ���� �������� blank=True, ����� �������� �������� ������ ��������.
    # ��� blank=False - ���� �����������.
    title = models.CharField(_('kind_title'), max_length=128, unique=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'kind'
    def __str__(self):
        # ����� ��������� ��� SELECT 
        return "{}".format(self.title)

# �������
class Client(models.Model):
    name = models.CharField(_('client_name'), max_length=128)
    address = models.CharField(_('client_address'), max_length=128)
    phone = models.CharField(_('client_phone'), max_length=32)
    email = models.CharField(_('client_email'), max_length=128)
    leader = models.CharField(_('client_leader'), max_length=128)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'client'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['name']),
        ]
        # ���������� �� ���������
        ordering = ['name']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}, {}, {}".format(self.name, self.phone, self.email)

#  ������ �������
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    client = models.ForeignKey(Client, related_name='application_client', on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, related_name='application_kind', on_delete=models.CASCADE)
    title = models.CharField(_('application_title'), max_length=255)
    details = models.TextField(_('application_details'))
    price = models.DecimalField(_('application_price'), max_digits=9, decimal_places=2)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'application'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['client']),
        ]
        # ���������� �� ���������
        ordering = ['datea']
    def __str__(self):
        # ����� � ��� Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.client, self.title)

# ��������� ��������� 
class Coming(models.Model):
    datec = models.DateTimeField(_('datec'))
    numb = models.IntegerField(_('numb'))     
    organization = models.CharField(_('organization'), max_length=256)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'coming'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datec']),            
        ]
        # ���������� �� ���������
        ordering = ['datec']
    def __str__(self):
        # ����� �������� � ��� SELECT 
        return "#{} {}".format(self.numb, self.datec)

# ������������� ��������� ��������� 
class ViewComing(models.Model):
    datec = models.DateTimeField(_('datec'))
    numb = models.IntegerField(_('numb'))     
    organization = models.CharField(_('organization'), max_length=256)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_coming'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datec']),
        ]
        # ���������� �� ���������
        ordering = ['datec']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "#{} {}".format(self.numb, self.datec)

# ��������� ������
class Category(models.Model):
    title = models.CharField(_('category_title'), max_length=128, unique=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'category'
    def __str__(self):
        # ����� ��������� ��� SELECT 
        return "{}".format(self.title)

# ������� �������
class Catalog(models.Model):
    coming = models.ForeignKey(Coming, related_name='catalog_coming', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='catalog_category', on_delete=models.CASCADE)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('catalog_price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)

# ������������� ���� ������ ������� �������
class ViewCatalog(models.Model):
    coming_id = models.IntegerField(_('coming_id'))
    category_id = models.IntegerField(_('category_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    sale_quantity = models.IntegerField(_('sale_quantity'))
    available = models.IntegerField(_('available'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_catalog'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['title']),
        ]
        # ���������� �� ���������
        ordering = ['title']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "{} {} {}".format(self.category, self.title, self.price)
    
# ��������� ��������� 
class Outgo(models.Model):
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    consumer = models.CharField(_('consumer'), max_length=256)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'outgo'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateo']),            
        ]
        # ���������� �� ���������
        ordering = ['dateo']
    def __str__(self):
        # ����� �������� � ��� SELECT 
        return "#{} {}".format(self.numb, self.dateo)
        # Override the save method of the model

 # ������������� ��������� ��������� 
class ViewOutgo(models.Model):
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    consumer = models.CharField(_('consumer'), max_length=256)
    total = models.IntegerField(_('total')) 
    #total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_outgo'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['dateo']),
        ]
        # ���������� �� ���������
        ordering = ['dateo']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "#{} {}".format(self.numb, self.dateo)

# ������� 
class Sale(models.Model):
    outgo = models.ForeignKey(Outgo, related_name='sale_outgo', on_delete=models.CASCADE)
    catalog = models.ForeignKey(Catalog, related_name='sale_catalog', on_delete=models.CASCADE)
    quantity = models.IntegerField(_('quantity'), default=1)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'sale'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['outgo']),
            models.Index(fields=['catalog']),
        ]
        # ���������� �� ���������
        ordering = ['outgo']
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}".format(self.catalog, self.quantity)
        # ������� �� ���� �� ��������� �� �������
        #managed = False

# ������������� ������� 
class ViewSale(models.Model):
    outgo_id = models.IntegerField(_('outgo_id'))
    dateo = models.DateTimeField(_('dateo'))
    numb = models.IntegerField(_('numb'))     
    consumer = models.CharField(_('consumer'), max_length=256)
    catalog_id = models.IntegerField(_('catalog_id'))
    category = models.CharField(_('category_title'), max_length=128)
    title = models.CharField(_('catalog_title'), max_length=255)
    details = models.TextField(_('catalog_details'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=9, decimal_places=2)
    quantity = models.IntegerField(_('quantity'))
    unit = models.CharField(_('unit'), max_length=32)
    total = models.DecimalField(_('total'), max_digits=9, decimal_places=2, blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_sale'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['outgo_id']),
            models.Index(fields=['catalog_id']),
        ]
        # ���������� �� ���������
        ordering = ['outgo_id']
        # ������� �� ���� �� ��������� �� �������
        managed = False
    def __str__(self):
        # ����� � ��� SELECT 
        return "{}: {}".format(self.catalog_id, self.quantity)
        # ������� �� ���� �� ��������� �� �������
        #managed = False

# ��������� 
class Message(models.Model):
    datem = models.DateTimeField(_('datem'), auto_now_add=True)
    sender = models.ForeignKey(User, related_name='sender_message', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_message', on_delete=models.CASCADE)
    details = models.TextField(_('message_details'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'message'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['recipient']),
        ]
        # ���������� �� ���������
        ordering = ['-datem']

# ������������� ���� ������ ���������
class ViewMessage(models.Model):
    id = models.IntegerField(_('message_id'), primary_key=True)
    datem = models.DateTimeField(_('datem'))
    sender_id = models.IntegerField(_('sender_id'))
    sender_username = models.CharField(_('sender_username'), max_length=150)
    sender_first_name = models.CharField(_('sender_first_name'), max_length=150, blank=True, null=True)
    sender_last_name = models.CharField(_('sender_last_name'), max_length=150, blank=True, null=True)
    recipient_id = models.IntegerField(_('recipient_id'))
    recipient_username = models.CharField(_('recipient_username'), max_length=150)
    recipient_first_name = models.CharField(_('recipient_first_name'), max_length=150, blank=True, null=True)
    recipient_last_name = models.CharField(_('recipient_last_name'), max_length=150, blank=True, null=True)
    details = models.TextField(_('message_details'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_message'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['datem']),
        ]
        # ���������� �� ���������
        ordering = ['datem']
        # ������� �� ���� �� ��������� �� �������
        managed = False

# ������������� ���� ������ ������������ + ��������� ����������� � ��������� �������� ���������
class ViewUserLastMessage(models.Model):
    id = models.IntegerField(_('auth_user_id'), primary_key=True)
    is_superuser =  models.BooleanField(_('is_superuser'), blank=True, null=True)
    username = models.CharField(_('username'), max_length=150)
    first_name = models.CharField(_('first_name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last_name'), max_length=150, blank=True, null=True)
    last_send_id = models.IntegerField(_('last_send_id'), blank=True, null=True)
    last_send_message = models.TextField(_('last_send_message'), blank=True, null=True)
    last_recipient_id = models.IntegerField(_('last_recipient_id'), blank=True, null=True)
    last_recipient_message = models.TextField(_('last_recipient_message'), blank=True, null=True)
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'view_user_last_message'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['username']),
        ]
        # ���������� �� ���������
        ordering = ['username']
        # ������� �� ���� �� ��������� �� �������
        managed = False

# ����������� 
class Notification(models.Model):
    start = models.DateTimeField(_('start'))
    finish = models.DateTimeField(_('finish'))
    title = models.CharField(_('notification_title'), max_length=256)
    details = models.TextField(_('notification_details'))
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'notification'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['start']),
            models.Index(fields=['finish']),
        ]
        # ���������� �� ���������
        ordering = ['start', 'finish']

# ������������� ����������
class ViewSaleYearMohtnTotal(models.Model):
    yr = models.IntegerField(_('yr'))     
    mon = models.IntegerField(_('mon'))     
    tot = models.IntegerField(_('tot'))     
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'sale_year_mohtn_total'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['yr']),
            models.Index(fields=['mon']),
        ]
        # ���������� �� ���������
        ordering = ['yr', 'mon']
        # ������� �� ���� �� ��������� �� �������
        managed = False

# ������������� ���������� 2
class ViewApplicationYearMohtnPrice(models.Model):
    yr = models.IntegerField(_('yr'))     
    mon = models.IntegerField(_('mon'))     
    tot = models.IntegerField(_('tot'))     
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'application_year_mohtn_price'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['yr']),
            models.Index(fields=['mon']),
        ]
        # ���������� �� ���������
        ordering = ['yr', 'mon']
        # ������� �� ���� �� ��������� �� �������
        managed = False


# ������� 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # ��������� ������
        # ��������������� ����� �������
        db_table = 'news'
        # indexes - ������ ��������, ������� ���������� ���������� � ������
        indexes = [
            models.Index(fields=['daten']),
        ]
        # ���������� �� ���������
        ordering = ['daten']
