from django.conf.urls import patterns, url

from ea_services import views

from ea_services.views import CredentialsView, UploadView

urlpatterns = [
    #points to the main page view
    url(r'^$', views.index, name='index'),
    url(r'^credentials/(?P<username>[A-Z0-9a-z\-]+)/$', CredentialsView.as_view()),
    url(r'^upload/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', UploadView.as_view())
]
