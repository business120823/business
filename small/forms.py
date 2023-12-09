from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Kind, Client, Application, Coming, Category, Catalog, ViewCatalog, Outgo, Sale, Notification, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.
# Категория заявки
class KindForm(forms.ModelForm):
    class Meta:
        model = Kind
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('kind_title'),            
        }
    # Метод-валидатор для поля title
    def clean_title(self):
        data = self.cleaned_data['title']
        # Ошибка если начинается не с большой буквы
        if data.istitle() == False:
            raise forms.ValidationError(_('Value must start with a capital letter'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Клиенты
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name','address','phone','email','leader',]
        widgets = {
            'name': TextInput(attrs={"size":"100"}),            
            'address': TextInput(attrs={"size":"80"}),
            'phone': TextInput(attrs={"size":"50", "type":"tel"}),            
            'email': TextInput(attrs={"size":"50", "type":"email"}), 
            'leader': TextInput(attrs={"size":"100"}),
        }
        labels = {
            'title': _('client_title'),            
        }

# Заказы клиента    
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        #fields = ('datea','client','kind','title', 'details', 'price')
        fields = ('client','kind','title', 'details', 'price')
        widgets = {
            #'datea': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'client': forms.Select(attrs={'class': 'chosen'}),            
            'kind': forms.Select(attrs={'class': 'chosen'}),            
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),     
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
        }        
        labels = {
            'client': _('client'),
            'kind': _('kind'),
        }

# Приходные накладные  
class ComingForm(forms.ModelForm):
    class Meta:
        model = Coming
        fields = ('organization', 'datec', 'numb',)
        widgets = {
            'organization': TextInput(attrs={"size":"100"}),
            'datec': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
        }
    # Метод-валидатор для поля datec
    def clean_datec(self):
        data = self.cleaned_data['datec']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

# Категория товара
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('category_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data
    
class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ('category', 'title', 'details', 'price', 'quantity', 'unit')
        widgets = {
            'category': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 5}),            
            'price': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'quantity': NumberInput(attrs={"size":"10", "min": "1", "step": "1"}),
            'unit': TextInput(attrs={"size":"50"}),
        }
        labels = {
            'category': _('category'),            
        }
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля price
    def clean_price(self):
        data = self.cleaned_data['price']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Price must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data       
    
# Расходные накладные  
class OutgoForm(forms.ModelForm):
    class Meta:
        model = Outgo
        fields = ('consumer', 'dateo', 'numb',)
        widgets = {
            'consumer': TextInput(attrs={"size":"100"}),
            'dateo': DateInput(attrs={"type":"date"}),
            'numb': DateInput(attrs={"type":"number"}),
        }
    # Метод-валидатор для поля dateo
    def clean_dateo(self):
        data = self.cleaned_data['dateo']
        #print(data)
        #print(timezone.now())
        # Проверка даты (не больше текущей даты-времени)
        if data > timezone.now():
            raise forms.ValidationError(_('Cannot be greater than the current date'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data
    # Метод-валидатор для поля numb
    def clean_numb(self):
        data = self.cleaned_data['numb']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('The number must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data        

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('catalog', 'quantity')
        widgets = {
            'catalog': forms.Select(attrs={'class': 'chosen'}),
            'quantity': NumberInput(attrs={"size":"10"}),            
        }
        labels = {
            'catalog': _('catalog'),            
        }
    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        available = ViewCatalog.objects.filter(available__gt=0).only('id').all()
        self.fields['catalog'].queryset = Catalog.objects.filter(id__in = available)
    # Метод-валидатор для поля numb
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        #print(data)
        # Проверка номер больше нуля
        if data <= 0:
            raise forms.ValidationError(_('Quantity must be greater than zero'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data

# Уведомления
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('start', 'finish', 'title', 'details')
        widgets = {
            'start': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'finish': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля start
    def clean_start(self):        
        if isinstance(self.cleaned_data['start'], datetime) == True:
            data = self.cleaned_data['start']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   
    # Метод-валидатор для поля finish
    def clean_finish(self):        
        if isinstance(self.cleaned_data['finish'], datetime) == True:
            data = self.cleaned_data['finish']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
