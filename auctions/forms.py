from django import forms

#Your forms here
class ItemForm(forms.Form):
    name = forms.CharField(max_length=64)
    descricao_curta = forms.CharField(max_length=64)
    descricao = forms.CharField()
    foto = forms.ImageField()
    preco = forms.DecimalField()
    categoria = forms.IntegerField(required=False)

class OfertaForm(forms.Form):
    preco = forms.DecimalField()
    password = forms.CharField()
    item_id = forms.IntegerField()

class ComentarioForm(forms.Form):
    name = forms.CharField(max_length=64)
    text = forms.CharField()
    item_id = forms.IntegerField()

class EditItemForm(forms.Form):
    name = forms.CharField(max_length=64)
    descricao_curta = forms.CharField(max_length=64)
    descricao = forms.CharField()
    foto = forms.ImageField()
    categoria = forms.IntegerField(required=False)
    status_venda = forms.BooleanField(required=False)