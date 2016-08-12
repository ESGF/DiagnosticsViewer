from django.conf.urls import patterns, url

from ea_services import views

urlpatterns = [
    url(r'^users/search/$', views.search_users, name="user-search"),
    url(r'^group/(?P<gid>\d+)/remove_user/$', views.remove_user_from_group, name="remove-user-from-group"),
    url(r'^group/(?P<gid>\d+)/add_user/$', views.add_user_to_group, name="add-user-to-group"),
    url(r'^group/share_dataset/$', views.share_dataset, name="share-dataset"),
    url(r'^credentials/(?P<username>[A-Z0-9a-z\-]+)/$', views.retrieve_key),
    url(r'^upload/(?P<dataset_name>[^/]+)/$', views.upload_files)
]
