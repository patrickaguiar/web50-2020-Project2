from django.db import models
from django.contrib.auth.models import User
import datetime

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=64, default='')
    foto = models.ImageField(upload_to='auctions_image/')
    preco_original = models.DecimalField(decimal_places=2, max_digits=9)
    preco_atual = models.DecimalField(decimal_places=2, max_digits=9)
    status_venda = models.BooleanField(default=False)
    item_star = models.BooleanField(default=False)
    quantidade_comentarios = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}: {self.name}'

class UserLista(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lista = models.ManyToManyField(Item) 

class Oferta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    preco = models.DecimalField(decimal_places=2, max_digits=9)
    status = models.BooleanField(default=False)

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=True, null=True)
    text = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

class Categoria(models.Model):
    name = models.CharField(max_length=64)
    lista = models.ManyToManyField(Item)
    foto = models.ImageField(upload_to='category_image/')

    def __str__(self):
        return f'{self.name}'