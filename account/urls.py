from django.conf.urls import patterns, url
from account import views

urlpatterns = patterns('',
    url(r'^create_account/', views.new_account, name='new_account'),
    url(r'^create/', views.create, name='create'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^login_page/', views.login_page, name='login_page'),
    url(r'^login/', views.login, name='login')
)