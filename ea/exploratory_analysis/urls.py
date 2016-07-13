from django.conf.urls import patterns, url
from exploratory_analysis import views

urlpatterns = [

    # Index page
    url(r'^$', views.index, name='index'),

    # Authentication views
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    url(r'^auth/$', views.auth, name='auth'),

    # Group views
    url(r'^group/membership/$', views.view_group_memberships, name="view-groups"),
    url(r'^group/(?P<group_id>\d+)/invite/$', views.invite_to_group, name="invite-to-group"),
    url(r'^group/(?P<group_id>\d+)/leave/$', views.leave_group, name="leave-group"),
    url(r'^group/create/$', views.create_group, name="create-group"),

    # output_viewer
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/$', views.output, name="output"),
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/(?P<path>.*)$', views.output_file, name="output_file"),
    url(r'^browse/', views.browse_datasets, name="browse_datasets"),
]


# service API for retrieving dataset variables
# url(r'^dataset_variables/(?P<dataset_name>\w+)/$', views.dataset_variables, name='dataset_variables'),


# service API for retrieving dataset pacakages
# url(r'^dataset_packages/(?P<dataset_name>\w+)/$', views.dataset_packages, name='dataset_packages'),