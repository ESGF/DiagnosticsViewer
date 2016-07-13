from django.conf.urls import patterns, url
from exploratory_analysis import views

urlpatterns = [

    # points to the main page view
    url(r'^$', views.index, name='index'),

    # login view
    url(r'^login/$', views.login_page, name='login_page'),

    # logout view
    url(r'^logout/$', views.logout_page, name='logout_page'),

    # auth view
    url(r'^auth/$', views.auth, name='auth'),

    # output_viewer
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/$', views.output, name="output"),
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/(?P<path>.*)$', views.output_file, name="output_file"),
    url(r'^browse/', views.browse_datasets, name="browse_datasets"),
]


# service API for retrieving dataset variables
# url(r'^dataset_variables/(?P<dataset_name>\w+)/$', views.dataset_variables, name='dataset_variables'),


# service API for retrieving dataset pacakages
# url(r'^dataset_packages/(?P<dataset_name>\w+)/$', views.dataset_packages, name='dataset_packages'),