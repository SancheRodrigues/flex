from django.db import models

class Shopee(models.Model):
    data = models.DateTimeField(auto_now_add=True) 
    quantidade = models.IntegerField()
    documento = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    assinatura = models.TextField()

    def save(self, *args, **kwargs):
 
        super().save(*args, **kwargs)


    class Meta:
        db_table = "shopee"

class MercadoLivre(models.Model):
    data = models.DateTimeField(auto_now_add=True) 
    quantidade = models.IntegerField()
    documento = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    assinatura = models.TextField()

    def save(self, *args, **kwargs):
 
        super().save(*args, **kwargs)


    class Meta:
        db_table = "mercadolivre"
