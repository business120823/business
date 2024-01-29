"""
URL configuration for business project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from small import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    #path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('kind/index/', views.kind_index, name='kind_index'),
    path('kind/create/', views.kind_create, name='kind_create'),
    path('kind/edit/<int:id>/', views.kind_edit, name='kind_edit'),
    path('kind/delete/<int:id>/', views.kind_delete, name='kind_delete'),
    path('kind/read/<int:id>/', views.kind_read, name='kind_read'),

    path('client/index/', views.client_index, name='client_index'),
    path('client/create/', views.client_create, name='client_create'),
    path('client/edit/<int:id>/', views.client_edit, name='client_edit'),
    path('client/delete/<int:id>/', views.client_delete, name='client_delete'),
    path('client/read/<int:id>/', views.client_read, name='client_read'),

    path('application/index/', views.application_index, name='application_index'),
    path('application/create/', views.application_create, name='application_create'),
    path('application/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('application/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('application/read/<int:id>/', views.application_read, name='application_read'),

    path('coming/index/', views.coming_index, name='coming_index'),
    path('coming/create/', views.coming_create, name='coming_create'),
    path('coming/edit/<int:id>/', views.coming_edit, name='coming_edit'),
    path('coming/delete/<int:id>/', views.coming_delete, name='coming_delete'),
    path('coming/read/<int:id>/', views.coming_read, name='coming_read'),

    path('category/index/', views.category_index, name='category_index'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/read/<int:id>/', views.category_read, name='category_read'),

    path('catalog/index/<int:coming_id>/', views.catalog_index, name='catalog_index'),
    path('catalog/list/', views.catalog_list, name='catalog_list'),
    path('catalog/create/<int:coming_id>/', views.catalog_create, name='catalog_create'),
    path('catalog/edit/<int:id>/<int:coming_id>/', views.catalog_edit, name='catalog_edit'),
    path('catalog/delete/<int:id>/<int:coming_id>/', views.catalog_delete, name='catalog_delete'),
    path('catalog/read/<int:id>/<int:coming_id>/', views.catalog_read, name='catalog_read'),
    path('catalog/details/<int:id>/', views.catalog_details, name='catalog_details'),    

    path('outgo/index/', views.outgo_index, name='outgo_index'),
    path('outgo/create/', views.outgo_create, name='outgo_create'),
    path('outgo/edit/<int:id>/', views.outgo_edit, name='outgo_edit'),
    path('outgo/delete/<int:id>/', views.outgo_delete, name='outgo_delete'),
    path('outgo/read/<int:id>/', views.outgo_read, name='outgo_read'),

    path('sale/index/<int:outgo_id>/', views.sale_index, name='sale_index'),
    path('sale/create/<int:outgo_id>/', views.sale_create, name='sale_create'),
    path('sale/edit/<int:id>/<int:outgo_id>/', views.sale_edit, name='sale_edit'),
    path('sale/delete/<int:id>/<int:outgo_id>/', views.sale_delete, name='sale_delete'),
    path('sale/read/<int:id>/<int:outgo_id>/', views.sale_read, name='sale_read'),

    path('message/index/', views.message_index, name='message_index'),
    path('message/list/', views.message_list, name='message_list'),
    path('message/send/<int:id>/', views.message_send, name='message_send'),

    path('notification/index/', views.notification_index, name='notification_index'),
    path('notification/list/', views.notification_list, name='notification_list'),
    path('notification/create/', views.notification_create, name='notification_create'),
    path('notification/edit/<int:id>/', views.notification_edit, name='notification_edit'),
    path('notification/delete/<int:id>/', views.notification_delete, name='notification_delete'),
    path('notification/read/<int:id>/', views.notification_read, name='notification_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.logoutUser, name="logout"),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
