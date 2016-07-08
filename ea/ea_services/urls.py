from django.conf.urls import patterns, url

from ea_services import views

from ea_services.views import PackagesView, Dataset_AccessView, PublishedView, VariablesView, CredentialsView, UploadView

urlpatterns = [
    #points to the main page view
    url(r'^$', views.index, name='index'),
    url(r'^dataset_packages/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', PackagesView.as_view()),
    url(r'^dataset_access/(?P<group_name>[A-Z0-9a-z\-]+)/$', Dataset_AccessView.as_view()),
    url(r'^published/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', PublishedView.as_view()),
    url(r'^variables/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', VariablesView.as_view()),
    url(r'^credentials/(?P<username>[A-Z0-9a-z\-]+)/$', CredentialsView.as_view()),
    url(r'^upload/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', UploadView.as_view())
]
