from django.conf.urls import patterns, url

from ea_services import views

from ea_services.views import CredentialsView, UploadView

urlpatterns = [
    url(r'^users/search/$', views.search_users, name="user-search"),
    url(r'^group/(?P<gid>\d+)/remove_user/$', views.remove_user_from_group, name="remove-user-from-group"),
    url(r'^group/(?P<gid>\d+)/add_user/$', views.add_user_to_group, name="add-user-to-group"),
    url(r'^credentials/(?P<username>[A-Z0-9a-z\-]+)/$', CredentialsView.as_view()),
    url(r'^upload/(?P<dataset_name>[A-Z0-9a-z\-]+)/$', UploadView.as_view())
]
