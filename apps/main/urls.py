from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^login$', views.login, name='login'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^view/(?P<id>\d+)$', views.view, name='view'),
    url(r'^make_job$', views.make_job, name='make_job'),
    url(r'^submit_the_job$', views.submit_the_job, name='submit_the_job'),
    url(r'^add_job(?P<id>\d+)$', views.add_job, name='add_job'),
    url(r'^edit_job(?P<id>\d+)$', views.edit_job, name='edit_job'),    
    url(r'^edit(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^cancel(?P<id>\d+)$', views.cancel, name='cancel'),
    url(r'^done(?P<id>\d+)$', views.done, name='done'), 
    url(r'^back$', views.back, name='back'),
    url(r'^logout$', views.logout, name='logout')
]
