from django.conf.urls import patterns, url

from ea_services import views

from ea_services.views import CredentialsView, UploadView

urlpatterns = [
    url(r'^users/search/$', views.search_users, name="search-users"),
    url(r'^credentials/(?P<username>[A-Z0-9a-z\-]+)/$', CredentialsView.as_view()),
    url(r'^upload/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', UploadView.as_view())
]
