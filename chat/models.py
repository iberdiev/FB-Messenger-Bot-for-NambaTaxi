from django.db import models

# Create your models here.
class Order(models.Model):

    ip_as_id = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 13)
    address = models.CharField(max_length = 50)
    tariff = models.CharField(max_length = 10)
    status = models.CharField(max_length = 10, default = 'Ищем водителей')
    bort = models.CharField(max_length = 50)

    def __str__(self):
        return '%s' % (self.ip_as_id)
