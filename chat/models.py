from django.db import models

# Create your models here.
class Order(models.Model):
    ip_as_id = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 13)
    address = models.CharField(max_length = 50)
    order_id = models.IntegerField(max_length = 30, null = True)
    tariff = models.CharField(max_length = 10, null = True)
    status = models.CharField(max_length = 20, default = 'Ищем водителей')

    def __str__(self):
        return '%s' % (self.ip_as_id)
