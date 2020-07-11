from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from django.db import IntegrityError

from .models import *
from .forms import *

class DataGetter(object):
    @staticmethod
    def get_itens():
        return Item.objects.all()[::-1]

    @staticmethod
    def get_item(item_id):
        return Item.objects.get(id=item_id)
        
    @staticmethod
    def get_user_itens(user_id):
        return Item.objects.filter(user__id=user_id)[::-1]

    @staticmethod
    def get_user_item(user_id, item_id):
        return Item.objects.filter(user=User.objects.get(id=user_id), id=item_id)

    @staticmethod
    def get_user_lista(user_id):
        watchlist = UserLista.objects.filter(user__id=user_id)[::-1]
        if watchlist:
            return watchlist[0].lista.all()
        else:
            return None

    @staticmethod
    def get_user_list_item(user_id, item_id):
        return UserLista.objects.filter(user__id=user_id, lista__id=item_id)

    @staticmethod
    def get_most_commented():
        return Item.objects.order_by('-quantidade_comentarios')

    @staticmethod
    def get_star():
        return Item.objects.filter(item_star=True)[::-1]

    @staticmethod
    def get_categories():
        return Categoria.objects.all()

    @staticmethod
    def get_category_itens(category_id):
        itens = Categoria.objects.get(id=category_id)
        if itens:
            return itens.lista.all()[::-1]
        else:
            return None

    @staticmethod
    def get_ofertas(item_id):
        return Oferta.objects.filter(item__id=item_id).order_by('-preco')

    @staticmethod
    def get_comentarios(item_id):
        return Comentario.objects.filter(item__id=item_id)[::-1]

class DataSetter(object):
    @staticmethod
    def register(username, first_name, last_name, email, password):
        try:
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, 
                    email=email, password=password)
            return True
        except IntegrityError:
            return False  

    @staticmethod
    def ItemSetter(DataValidation, user_id):
        if DataValidation.is_valid():
            name = DataValidation.cleaned_data['name']
            descricao_curta = DataValidation.cleaned_data['descricao_curta']
            descricao = DataValidation.cleaned_data['descricao']
            foto = DataValidation.cleaned_data['foto']
            preco = DataValidation.cleaned_data['preco']
            categoria = DataValidation.cleaned_data['categoria']

            NovoItem = Item.objects.create(user=User.objects.get(id=user_id) ,name=name, descricao_curta=descricao_curta, 
                                descricao=descricao, foto=foto, preco_original=preco, preco_atual=preco)

            if categoria:
                Categoria.objects.get(id=categoria).lista.add(NovoItem)
            
            return True
        else:
            return False

    @staticmethod
    def set_oferta(form, user_id, user_password):
        password = form.cleaned_data['password']
        preco = form.cleaned_data['preco']
        item = Item.objects.get(id=form.cleaned_data['item_id'])

        if item.status_venda:
            return False
        
        if not check_password(password, user_password):
            return False
        else:
            if preco > item.preco_atual:
                Oferta.objects.create(user=User.objects.get(id=user_id), item=item, preco=preco)
                item.preco_atual = preco
                item.save()
                return True
            else:
                return False

    @staticmethod
    def set_comentario(form, user_id):
        name = form.cleaned_data['name']
        text = form.cleaned_data['text']
        item_id = form.cleaned_data['item_id']

        Comentario.objects.create(user=User.objects.get(id=user_id), item=Item.objects.get(id=item_id),
                                    name=name, text=text)

    
    @staticmethod
    def add_watchlist(item_id, user_id):
        user = User.objects.get(id=user_id)
        item = Item.objects.get(id=item_id)
        watchlist = UserLista.objects.filter(user__id=user_id)

        if watchlist:
            watchlist[0].lista.add(item)
        else:
            UserLista.objects.create(user=user)
            UserLista.objects.get(user=user).lista.add(item)


    @staticmethod
    def remove_watchlist(item_id, user_id):
        item = Item.objects.get(id=item_id)
        user = User.objects.get(id=user_id)
        watchlist = UserLista.objects.get(user=user).lista.remove(item)

    @staticmethod
    def edit_item(DataValidation, item_id):
        item = Item.objects.get(id=item_id)

        if item.status_venda:
            return False

        item.name = DataValidation.cleaned_data['name']
        item.descricao_curta = DataValidation.cleaned_data['descricao_curta']
        item.descricao = DataValidation.cleaned_data['descricao']
        item.foto = DataValidation.cleaned_data['foto']
        item.status_venda = DataValidation.cleaned_data['status_venda']
        item.save()

        return True

    @staticmethod
    def delete_listing(item_id, user_id):
        item = Item.objects.get(id=item_id)
        user = User.objects.get(id=user_id)
            
        if item.user == user:
            item.delete()
            return True

        return False
            

# Create your views here.
def index_view(request):
    itens = DataGetter.get_itens()

    if request.user.is_authenticated:
        return render(request, 'user_in/index.html', {
            'itens': itens,
        })
    else:
        return render(request, 'user_out/index.html', {
            'itens': itens,
        })

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user_validation = authenticate(request, username=username, password=password)
            if user_validation is not None:
                login(request, user_validation)
                return redirect('index')
            else:
                return render(request, 'user_out/login.html', {
                    'message':'Incorrect username or password.'
                })
        else:
            return render(request, 'user_out/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            if request.POST["password"] == request.POST["confirmation"]:
                username = request.POST["username"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                email = request.POST["email"]
                password = request.POST["password"]

                if DataSetter.register(username, first_name, last_name, email, password):
                    message = 'You\'re now at eBay50!'
                else:
                    message = 'Username alredy taken.'
            else:
                message = 'Passwords must match.'
            
            return render(request, 'user_out/register.html', {
                'message':message
            })

    return render(request, 'user_out/register.html')

@login_required
def create_listing(request):
    categories = DataGetter.get_categories()
    if request.method == 'POST':
        DataValidation = ItemForm(request.POST, request.FILES)
        if DataSetter.ItemSetter(DataValidation, request.user.id):
            return redirect('my_listings')
        else:
            return render(request, 'user_in/create_listing.html', {
                'categories':categories, 'message':'Plese, fill all the fields.'
            })
    else:
        return render(request, 'user_in/create_listing.html', {
            'categories':categories
        })

@login_required
def my_listings(request):
    itens = DataGetter.get_user_itens(request.user.id)
    return render(request, 'user_in/index.html', {'itens': itens,})

@login_required
def watchlist(request):
    itens = DataGetter.get_user_lista(request.user.id)
    return render(request, 'user_in/index.html', {'itens': itens,})


def most_commented(request):
    itens = DataGetter.get_most_commented()
    if request.user.is_authenticated:
        return render(request, 'user_in/index.html', {'itens': itens,})
    else:
        return render(request, 'user_out/index.html', {'itens': itens,})

def star(request):
    itens = DataGetter.get_star()
    if request.user.is_authenticated:
        return render(request, 'user_in/index.html', {'itens': itens,})
    else:
        return render(request, 'user_out/index.html', {'itens': itens,})

def categories(request):
    categories = DataGetter.get_categories()
    if request.user.is_authenticated:
        return render(request, 'user_in/categories.html', {'categories':categories})
    else:
        return render(request, 'user_out/categories.html', {'categories':categories})

def categories_id(request, category_id):
    itens = DataGetter.get_category_itens(category_id)
    if request.user.is_authenticated:
        return render(request, 'user_in/index.html', {'itens': itens,})
    else:
        return render(request, 'user_out/index.html', {'itens': itens,})

def item(request, item_id):
    item = DataGetter.get_item(item_id)
    ofertas = DataGetter.get_ofertas(item_id)
    comentarios = DataGetter.get_comentarios(item_id)

    if request.user.is_authenticated:
        return render(request, 'user_in/item.html', {'item':item, 'ofertas':ofertas, 'comentarios':comentarios,
                                                    'watchlist':DataGetter.get_user_list_item(request.user.id, item_id),
                                                    'my_item':DataGetter.get_user_item(request.user.id, item_id)})
    else:
        return render(request, 'user_out/item.html', {'item':item, 'ofertas':ofertas, 'comentarios':comentarios,})

@login_required
def oferta(request):
    item_id = request.POST['item_id']
    item = DataGetter.get_item(item_id)
    ofertas = DataGetter.get_ofertas(item_id)
    comentarios = DataGetter.get_comentarios(item_id)

    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            if DataSetter.set_oferta(form, request.user.id, request.user.password):
                return redirect('item', item_id=item_id)
            else:
                return render(request, 'user_in/item.html', {
                'message_oferta': 'Please, verify your password and remember: Your bid needs to be greater than the current price.',
                'item': item, 'ofertas':ofertas, 'comentarios':comentarios,
                'watchlist':DataGetter.get_user_list_item(request.user.id, item_id),
                'my_item':DataGetter.get_user_item(request.user.id, item_id)
            })
        else:
            return render(request, 'user_in/item.html', {
                'message_oferta': 'Please, fill all the fields.',
                'item': item, 'ofertas':ofertas, 'comentarios':comentarios,
                'watchlist':DataGetter.get_user_list_item(request.user.id, item_id),
                'my_item':DataGetter.get_user_item(request.user.id, item_id)
            })
    else:
        return redirect('index')

@login_required
def comentario(request):
    item_id = request.POST['item_id']
    item = DataGetter.get_item(item_id)
    ofertas = DataGetter.get_ofertas(item_id)
    comentarios = DataGetter.get_comentarios(item_id)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            DataSetter.set_comentario(form, request.user.id)
            return redirect('item', item_id=item_id)
        else:
            return render(request, 'user_in/item.html', {
                'message_oferta': 'Please, Fill all the fields.',
                'item': item, 'ofertas':ofertas, 'comentarios':comentarios,
                'watchlist':DataGetter.get_user_list_item(request.user.id, item_id),
                'my_item':DataGetter.get_user_item(request.user.id, item_id)
            })
    else:
        return redirect('index')

@login_required
def add_watchlist(request, item_id):
    DataSetter.add_watchlist(item_id, request.user.id)
    return redirect('item', item_id=item_id)

@login_required
def remove_watchlist(request, item_id):
    DataSetter.remove_watchlist(item_id, request.user.id)
    return redirect('item', item_id=item_id)

@login_required
def edit_item(request, item_id):
    item = DataGetter.get_item(item_id)
    categories = DataGetter.get_categories()

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES)
        if form.is_valid():
            if DataSetter.edit_item(form, item_id):
                return redirect('item', item_id=item_id)
            else:
                return render(request, 'user_in/edit_item.html', {'item':item, 'categories':categories,
                                                                    'message':'Please, verify if you\'re logged in'})
        else:
            return render(request, 'user_in/edit_item.html', {'item':item, 'categories':categories, 
                                                                'message':'Please, fill all the fields'})
    else:
        if not DataGetter.get_user_item(request.user.id, item_id):
            return redirect('index')
        else:
            return render(request, 'user_in/edit_item.html', {'item':item, 'categories':categories})

@login_required
def delete_listing(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        DataSetter.delete_listing(item_id, request.user.id)
        return redirect('my_listings')
