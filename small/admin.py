from django.contrib import admin

from .models import Kind, Client, Application, Coming, Category, Catalog, Outgo, Sale, Message, Notification, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Kind)
admin.site.register(Client)
admin.site.register(Application)
admin.site.register(Coming)
admin.site.register(Category)
admin.site.register(Catalog)
admin.site.register(Outgo)
admin.site.register(Sale)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(News)
