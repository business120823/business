from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Kind, Client, Application, Coming, ViewComing, Category, Catalog, ViewCatalog, Outgo, ViewOutgo, Sale, ViewSale, Message, ViewMessage, ViewUserLastMessage, Notification, ViewSaleYearMohtnTotal, ViewApplicationYearMohtnPrice, News
# Подключение форм
from .forms import KindForm, ClientForm, ApplicationForm, ComingForm, CategoryForm, CatalogForm, OutgoForm, SaleForm, NotificationForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        # Статистика
        sale_year_mohtn_total = ViewSaleYearMohtnTotal.objects.order_by('yr').order_by('mon')
        application_year_mohtn_price = ViewApplicationYearMohtnPrice.objects.order_by('yr').order_by('mon')
        return render(request, "index.html", {"sale_year_mohtn_total": sale_year_mohtn_total, "application_year_mohtn_price": application_year_mohtn_price, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

## Отчеты
#@login_required
#@group_required("Managers")
#def report_index(request):
#    try:
#        catalog = ViewCatalog.objects.all().order_by('title')
#        sale = ViewSale.objects.all().order_by('saleday')
#        delivery = Delivery.objects.all().order_by('deliveryday')
#        review = ViewSale.objects.exclude(rating=None).order_by('category', 'title', 'saleday')
#        return render(request, "report/index.html", {"catalog": catalog, "sale": sale, "delivery": delivery, "review": review })    
#    except Exception as exception:
#        print(exception)
#        return HttpResponse(exception)    
###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def kind_index(request):
    try:
        kind = Kind.objects.all().order_by('title')
        return render(request, "kind/index.html", {"kind": kind,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def kind_create(request):
    try:
        if request.method == "POST":
            kind = Kind()
            kind.title = request.POST.get("title")
            kindform = KindForm(request.POST)
            if kindform.is_valid():
                kind.save()
                return HttpResponseRedirect(reverse('kind_index'))
            else:
                return render(request, "kind/create.html", {"form": kindform})
        else:        
            kindform = KindForm()
            return render(request, "kind/create.html", {"form": kindform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def kind_edit(request, id):
    try:
        kind = Kind.objects.get(id=id)
        if request.method == "POST":
            kind.title = request.POST.get("title")
            kindform = KindForm(request.POST)
            if kindform.is_valid():
                kind.save()
                return HttpResponseRedirect(reverse('kind_index'))
            else:
                return render(request, "kind/edit.html", {"form": kindform})
        else:
            # Загрузка начальных данных
            kindform = KindForm(initial={'title': kind.title, })
            return render(request, "kind/edit.html", {"form": kindform})
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def kind_delete(request, id):
    try:
        kind = Kind.objects.get(id=id)
        kind.delete()
        return HttpResponseRedirect(reverse('kind_index'))
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def kind_read(request, id):
    try:
        kind = Kind.objects.get(id=id) 
        return render(request, "kind/read.html", {"kind": kind})
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def client_index(request):
    try:
        client = Client.objects.all().order_by('name')
        return render(request, "client/index.html", {"client": client,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def client_create(request):
    try:
        if request.method == "POST":
            client = Client()
            client.name = request.POST.get("name")
            client.address = request.POST.get("address")
            client.phone = request.POST.get("phone")
            client.email = request.POST.get("email")
            client.leader = request.POST.get("leader")
            clientform = ClientForm(request.POST)
            if clientform.is_valid():
                client.save()
                return HttpResponseRedirect(reverse('client_index'))
            else:
                return render(request, "client/create.html", {"form": clientform})
        else:        
            clientform = ClientForm()
            return render(request, "client/create.html", {"form": clientform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def client_edit(request, id):
    try:
        client = Client.objects.get(id=id)
        if request.method == "POST":
            client.name = request.POST.get("name")
            client.address = request.POST.get("address")
            client.phone = request.POST.get("phone")
            client.email = request.POST.get("email")
            client.leader = request.POST.get("leader")
            clientform = ClientForm(request.POST)
            if clientform.is_valid():
                client.save()
                return HttpResponseRedirect(reverse('client_index'))
            else:
                return render(request, "client/edit.html", {"form": clientform})
        else:
            # Загрузка начальных данных
            clientform = ClientForm(initial={'name': client.name, 'address': client.address, 'phone': client.phone, 'email': client.email, 'leader': client.leader, })
            return render(request, "client/edit.html", {"form": clientform})
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def client_delete(request, id):
    try:
        client = Client.objects.get(id=id)
        client.delete()
        return HttpResponseRedirect(reverse('client_index'))
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def client_read(request, id):
    try:
        client = Client.objects.get(id=id) 
        return render(request, "client/read.html", {"client": client})
    except Client.DoesNotExist:
        return HttpResponseNotFound("<h2>Client not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = Application.objects.all().order_by('-datea')
        return render(request, "application/index.html", {"application": application,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.datea = request.POST.get("datea")
            application.client = Client.objects.filter(id=request.POST.get("client")).first()
            application.kind = Kind.objects.filter(id=request.POST.get("kind")).first()
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            application.price = request.POST.get("price")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm()
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id)
        if request.method == "POST":
            application = Application()
            application.datea = request.POST.get("datea")
            application.client = Client.objects.filter(id=request.POST.get("client")).first()
            application.kind = Kind.objects.filter(id=request.POST.get("kind")).first()
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            application.price = request.POST.get("price")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'datea': application.datea, 'client': application.client, 'kind': application.kind, 'title': application.title, 'details': application.details,  'price': application.price, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def application_read(request, id):
    try:
        application = Application.objects.get(id=id) 
        return render(request, "application/read.html", {"application": application})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
@login_required
@group_required("Managers")
def coming_index(request):
    coming = ViewComing.objects.all().order_by('-datec')
    return render(request, "coming/index.html", {"coming": coming,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def coming_create(request):
    try:
        if request.method == "POST":
            coming = Coming()
            coming.organization = request.POST.get("organization")
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb")
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/create.html", {"form": comingform})
        else:        
            comingform = ComingForm(initial={'datec': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "coming/create.html", {"form": comingform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def coming_edit(request, id):
    try:
        coming = Coming.objects.get(id=id)
        if request.method == "POST":
            coming.organization = request.POST.get("organization")
            coming.datec = request.POST.get("datec")
            coming.numb = request.POST.get("numb")   
            comingform = ComingForm(request.POST)
            if comingform.is_valid():
                coming.save()
                return HttpResponseRedirect(reverse('coming_index'))
            else:
                return render(request, "coming/edit.html", {"form": comingform})
        else:
            # Загрузка начальных данных
            comingform = ComingForm(initial={'datec': coming.datec.strftime('%Y-%m-%d'), 'organization': coming.organization,  'numb': coming.numb, })
            return render(request, "coming/edit.html", {"form": comingform})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def coming_delete(request, id):
    try:
        coming = Coming.objects.get(id=id)
        coming.delete()
        return HttpResponseRedirect(reverse('coming_index'))
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def coming_read(request, id):
    try:
        coming = ViewComing.objects.get(id=id) 
        return render(request, "coming/read.html", {"coming": coming})
    except Coming.DoesNotExist:
        return HttpResponseNotFound("<h2>Coming not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def category_index(request):
    try:
        category = Category.objects.all().order_by('title')
        return render(request, "category/index.html", {"category": category,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def category_create(request):
    try:
        if request.method == "POST":
            category = Category()
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/create.html", {"form": categoryform})
        else:        
            categoryform = CategoryForm()
            return render(request, "category/create.html", {"form": categoryform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def category_edit(request, id):
    try:
        category = Category.objects.get(id=id)
        if request.method == "POST":
            category.title = request.POST.get("title")
            categoryform = CategoryForm(request.POST)
            if categoryform.is_valid():
                category.save()
                return HttpResponseRedirect(reverse('category_index'))
            else:
                return render(request, "category/edit.html", {"form": categoryform})
        else:
            # Загрузка начальных данных
            categoryform = CategoryForm(initial={'title': category.title, })
            return render(request, "category/edit.html", {"form": categoryform})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def category_delete(request, id):
    try:
        category = Category.objects.get(id=id)
        category.delete()
        return HttpResponseRedirect(reverse('category_index'))
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def category_read(request, id):
    try:
        category = Category.objects.get(id=id) 
        return render(request, "category/read.html", {"category": category})
    except Category.DoesNotExist:
        return HttpResponseNotFound("<h2>Category not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def catalog_index(request, coming_id):
    #catalog = Catalog.objects.all().order_by('title')
    coming = ViewComing.objects.get(id=coming_id)
    catalog = ViewCatalog.objects.filter(coming_id=coming_id).order_by('title')
    return render(request, "catalog/index.html", {"catalog": catalog, "coming": coming, "coming_id": coming_id})
    
# Список для просмотра и отправки в корзину
#@login_required
#@group_required("Managers")
#@login_required
def catalog_list(request):
    try:
        # Каталог доступных товаров
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        # Категории и подкатегория товара (для поиска)
        category = Category.objects.all().order_by('title')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по категории товара
                selected_item_category = request.POST.get('item_category')
                #print(selected_item_category)
                if selected_item_category != '-----':
                    catalog = catalog.filter(category=selected_item_category).all()
                # Поиск по названию товара
                catalog_search = request.POST.get("catalog_search")
                #print(catalog_search)                
                if catalog_search != '':
                    catalog = catalog.filter(title__contains = catalog_search).all()
                # Сортировка
                sort = request.POST.get('radio_sort')
                #print(sort)
                direction = request.POST.get('checkbox_sort_desc')
                #print(direction)
                if sort=='title':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-title')
                    else:
                        catalog = catalog.order_by('title')
                elif sort=='price':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-price')
                    else:
                        catalog = catalog.order_by('price')
                elif sort=='category':                    
                    if direction=='ok':
                        catalog = catalog.order_by('-category')
                    else:
                        catalog = catalog.order_by('category')
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category, "selected_item_category": selected_item_category, "catalog_search": catalog_search, "sort": sort, "direction": direction,})    
            else:          
                return render(request, "catalog/list.html", {"catalog": catalog, "category": category,})    
        else:
            return render(request, "catalog/list.html", {"catalog": catalog, "category": category, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def catalog_create(request, coming_id):
    try:
        if request.method == "POST":
            catalog = Catalog()
            catalog.coming_id = coming_id
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/create.html", {"form": catalogform})
        else:        
            catalogform = CatalogForm()
            return render(request, "catalog/create.html", {"form": catalogform, "coming_id": coming_id})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def catalog_edit(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        if request.method == "POST":
            catalog.category = Category.objects.filter(id=request.POST.get("category")).first()
            catalog.title = request.POST.get("title")
            catalog.details = request.POST.get("details")        
            catalog.price = request.POST.get("price")
            catalog.quantity = request.POST.get("quantity")
            catalog.unit = request.POST.get("unit")
            catalogform = CatalogForm(request.POST)
            if catalogform.is_valid():
                catalog.save()
                return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
            else:
                return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})            
        else:
            # Загрузка начальных данных
            catalogform = CatalogForm(initial={'category': catalog.category, 'title': catalog.title, 'details': catalog.details, 'price': catalog.price, 'quantity': catalog.quantity, 'unit': catalog.unit, })
            #print('->',catalog.photo )
            return render(request, "catalog/edit.html", {"form": catalogform, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def catalog_delete(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id)
        catalog.delete()
        return HttpResponseRedirect(reverse('catalog_index', args=(coming_id,)))
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def catalog_read(request, id, coming_id):
    try:
        catalog = Catalog.objects.get(id=id) 
        return render(request, "catalog/read.html", {"catalog": catalog, "coming_id": coming_id})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для клиента
#@login_required
def catalog_details(request, id):
    try:
        # Товар с каталога
        catalog = ViewCatalog.objects.get(id=id)
        # Отзывы на данный товар
        #reviews = ViewSale.objects.filter(catalog_id=id).exclude(rating=None)
        return render(request, "catalog/details.html", {"catalog": catalog,})
    except Catalog.DoesNotExist:
        return HttpResponseNotFound("<h2>Catalog not found</h2>")

###################################################################################################

@login_required
@group_required("Managers")
def outgo_index(request):
    outgo = ViewOutgo.objects.all().order_by('-dateo')
    return render(request, "outgo/index.html", {"outgo": outgo,})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на коре# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def outgo_create(request):
    try:
        if request.method == "POST":
            outgo = Outgo()
            outgo.consumer = request.POST.get("consumer")
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/create.html", {"form": outgoform})
        else:        
            outgoform = OutgoForm(initial={'dateo': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "outgo/create.html", {"form": outgoform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def outgo_edit(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        if request.method == "POST":
            outgo.consumer = request.POST.get("consumer")
            outgo.dateo = request.POST.get("dateo")
            outgo.numb = request.POST.get("numb")   
            outgoform = OutgoForm(request.POST)
            if outgoform.is_valid():
                outgo.save()
                return HttpResponseRedirect(reverse('outgo_index'))
            else:
                return render(request, "outgo/edit.html", {"form": outgoform})
        else:
            # Загрузка начальных данных
            outgoform = OutgoForm(initial={'dateo': outgo.dateo.strftime('%Y-%m-%d'), 'consumer': outgo.consumer,  'numb': outgo.numb, })
            return render(request, "outgo/edit.html", {"form": outgoform})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def outgo_delete(request, id):
    try:
        outgo = Outgo.objects.get(id=id)
        outgo.delete()
        return HttpResponseRedirect(reverse('outgo_index'))
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def outgo_read(request, id):
    try:
        outgo = ViewOutgo.objects.get(id=id) 
        return render(request, "outgo/read.html", {"outgo": outgo})
    except Outgo.DoesNotExist:
        return HttpResponseNotFound("<h2>Outgo not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def sale_index(request, outgo_id):
    #sale = Sale.objects.all()
    outgo = ViewOutgo.objects.get(id=outgo_id)
    sale = ViewSale.objects.filter(outgo_id=outgo_id)
    return render(request, "sale/index.html", {"sale": sale, "outgo": outgo, "outgo_id": outgo_id})

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def sale_create(request, outgo_id):
    try:
        # Каталог доступных товаров
        catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
        if request.method == "POST":
            # Перебрать весь каталог смотреть отмеченные товары
            for cat in catalog:
                if request.POST.get("quantity" + str(cat.id)):
                    sale = Sale()
                    sale.outgo_id = outgo_id
                    sale.catalog_id = cat.id
                    sale.quantity = request.POST.get("quantity" + str(cat.id))
                    sale.save()
                    #print(f"{cat.id}.{cat.title} - {cat.available}")
            return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
        else:        
            saleform = SaleForm()
            return render(request, "sale/create.html", {"form": saleform, "outgo_id": outgo_id, "catalog": catalog})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    #try:
    #    # Каталог доступных товаров
    #    catalog = ViewCatalog.objects.filter(available__gt=0).order_by('category').order_by('title')
    #    if request.method == "POST":
    #        sale = Sale()
    #        sale.outgo_id = outgo_id
    #        sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
    #        #sale.catalog = ViewCatalog.objects.filter(id=request.POST.get("catalog")).first()
    #        sale.quantity = request.POST.get("quantity")
    #        saleform = SaleForm(request.POST)
    #        if saleform.is_valid():
    #            #sale.save()
    #            return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
    #        else:
    #            return render(request, "sale/create.html", {"form": saleform})
    #    else:        
    #        saleform = SaleForm()
    #        return render(request, "sale/create.html", {"form": saleform, "outgo_id": outgo_id, "catalog": catalog})
    #except Exception as exception:
    #    print(exception)
    #    return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def sale_edit(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        if request.method == "POST":
            sale.catalog = Catalog.objects.filter(id=request.POST.get("catalog")).first()
            sale.quantity = request.POST.get("quantity")
            saleform = SaleForm(request.POST)
            if saleform.is_valid():
                sale.save()
                return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
            else:
                return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})            
        else:
            # Загрузка начальных данных
            saleform = SaleForm(initial={'catalog': sale.catalog, 'quantity': sale.quantity, })
            #print('->',sale.photo )
            return render(request, "sale/edit.html", {"form": saleform, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def sale_delete(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return HttpResponseRedirect(reverse('sale_index', args=(outgo_id,)))
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы с информацией о товаре для менеджера.
@login_required
@group_required("Managers")
def sale_read(request, id, outgo_id):
    try:
        sale = Sale.objects.get(id=id) 
        return render(request, "sale/read.html", {"sale": sale, "outgo_id": outgo_id})
    except Sale.DoesNotExist:
        return HttpResponseNotFound("<h2>Sale not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        #news = News.objects.all().order_by('surname', 'name', 'patronymic')
        #return render(request, "news/index.html", {"news": news})
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/list.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']        
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:        
            #newsform = NewsForm(request.FILES, initial={'daten': datetime.now().strftime('%Y-%m-%d'),})
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            news.save()
            return HttpResponseRedirect(reverse('news_index'))
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def notification_index(request):
    try:
        #notification = Notification.objects.all().order_by('surname', 'name', 'patronymic')
        #return render(request, "notification/index.html", {"notification": notification})
        notification = Notification.objects.all().order_by('-start')
        return render(request, "notification/index.html", {"notification": notification})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# Список для просмотра
def notification_list(request):
    try:
        notification = Notification.objects.all().order_by('-start')
        return render(request, "notification/list.html", {"notification": notification})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def notification_create(request):
    try:
        if request.method == "POST":
            notification = Notification()        
            notification.start = request.POST.get("start")
            notification.finish = request.POST.get("finish")
            notification.title = request.POST.get("title")
            notification.details = request.POST.get("details")
            notification.save()
            return HttpResponseRedirect(reverse('notification_index'))
        else:        
            #notificationform = NotificationForm(request.FILES, initial={'start': datetime.now().strftime('%Y-%m-%d'),})
            notificationform = NotificationForm(initial={'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "notification/create.html", {"form": notificationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def notification_edit(request, id):
    try:
        notification = Notification.objects.get(id=id) 
        if request.method == "POST":
            notification.start = request.POST.get("start")
            notification.finish = request.POST.get("finish")
            notification.title = request.POST.get("title")
            notification.details = request.POST.get("details")
            notification.save()
            return HttpResponseRedirect(reverse('notification_index'))
        else:
            # Загрузка начальных данных
            notificationform = NotificationForm(initial={'start': notification.start.strftime('%Y-%m-%d %H:%M:%S'), 'finish': notification.finish.strftime('%Y-%m-%d %H:%M:%S'), 'title': notification.title, 'details': notification.details, })
            return render(request, "notification/edit.html", {"form": notificationform})
    except Notification.DoesNotExist:
        return HttpResponseNotFound("<h2>Notification not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def notification_delete(request, id):
    try:
        notification = Notification.objects.get(id=id)
        notification.delete()
        return HttpResponseRedirect(reverse('notification_index'))
    except Notification.DoesNotExist:
        return HttpResponseNotFound("<h2>Notification not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def notification_read(request, id):
    try:
        notification = Notification.objects.get(id=id) 
        return render(request, "notification/read.html", {"notification": notification})
    except Notification.DoesNotExist:
        return HttpResponseNotFound("<h2>Notification not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################  

###################################################################################################  
# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def message_index(request):
    message = Message.objects.all().order_by('-datem')
    return render(request, "message/index.html", {"message": message})
  
# Список для просмотра
@login_required
def message_list(request):
    # Себя в списке не показывать, суперпользоватля тоже 
    my_id = request.user.id
    my_user = request.user.first_name + " " + request.user.last_name
    # Список пользователей + последние отправленные и принятые сообщения
    view_user_last_message = ViewUserLastMessage.objects.exclude(id=my_id).exclude(is_superuser=True).order_by('username')
    #view_user_last_message = ViewUserLastMessage.objects.filter(Q(last_send_id=my_id) | Q(last_recipient_id=my_id))
    return render(request, "message/list.html", {"view_user_last_message": view_user_last_message, "my_id": my_id, "my_user": my_user, })

@login_required
def message_send(request, id):
    # id текущего пользователя
    my_id = request.user.id
    try:
        recipient_user = User.objects.get(id=id)
        my_user = request.user
        message = Message.objects.filter(Q(sender_id=my_id) | Q(recipient_id=my_id)).filter(Q(sender_id=id) | Q(recipient_id=id)).order_by('-datem')
        if request.method == "POST":
            mes = Message()
            mes.sender_id = my_id
            mes.recipient_id = id
            mes.details = request.POST.get("message")
            mes.save()
            return HttpResponseRedirect(reverse('message_send', args=(id,)))
        else:
            return render(request, "message/send.html", {"recipient_user": recipient_user, "my_user": my_user, "message": message, "my_id": my_id, "user_id": id })
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")

## Список для отправки сообщений
#@login_required
#def message_list(request):
#        # id текущего пользователя
#    # id user текущего пользователя
#    my_user_id = request.user.id

#    try:
#        # id пользователя котрому отправляется сообщение
#        message = Message.objects.filter(Q(sender_id=my_user_id) | Q(recipient_id=my_user_id)).order_by('-datem')
#        if request.method == "POST":
#            mes = Message()
#            mes.sender_id = my_user_id
#            #mes.recipient_id = person_user_id
#            mes.details = request.POST.get("message")
#            mes.save()
#            return HttpResponseRedirect(reverse('person_read', args=(id,)))
#        else:
#            print("id", id)
#            #print("my_person_id", my_person_id)
#            return render(request, "message/list.html", {"message": message, "my_user_id": my_user_id, })
#            #return render(request, "person/read.html", {"person": person, "my_person": my_person, "my_status": my_status, "status_last": status_last, "message": message, "friend": friend, "my_friend": my_friend, "status": status, "photo": photo, "my_id": my_id, "person_id": id })
#    except Exception as exception:
#        print(exception)
#        return HttpResponse(exception)

## Список для изменения с кнопками создать, изменить, удалить
#@login_required
#@group_required("Managers")
#def message_index(request):
#    try:
#        message = Message.objects.all().order_by('-datem')
#        return render(request, "message/index.html", {"message": message})
#    except Exception as exception:
#        print(exception)
#        return HttpResponse(exception)

###################################################################################################    

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")



