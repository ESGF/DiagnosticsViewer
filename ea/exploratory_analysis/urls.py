from django.conf.urls import patterns, url
from exploratory_analysis import views

urlpatterns = [

    # points to the main page view
    url(r'^$', views.index, name='index'),

    # login view
    url(r'^login/$', views.login_page, name='login_page'),

    # logout view
    url(r'^logout/$', views.logout_page, name='logout_page'),

    # front end config
    url(r'^config/$', views.config, name='config'),

    # auth view
    url(r'^auth/$', views.auth, name='auth'),

    # auth view - no esgf
    url(r'^auth_noesgf/$', views.auth_noesgf, name='auth_noesgf'),

    # main page view
    url(r'^main/(?P<user_id>\w+)/$', views.main, name='main'),

    # proveance view
    url(r'^provenance/$', views.provenance, name='provenance'),

    # classic view
    url(r'^classic/(?P<user_id>\w+)/$', views.classic, name='classic'),

    # classic html block - main list of sets
    url(r'^classic_set_list_html/$', views.classic_set_list_html, name='classic_set_list_html'),

    # classic html block - specific set
    url(r'^classic_views_html/$', views.classic_views_html, name='classic_views_html'),

    # output_viewer
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/$', views.output, name="output"),
    url(r'^output/(?P<dataset>[^/]+)/(?P<package>[^/]+)/(?P<path>.*)$', views.output_file, name="output_file"),
]


# service API for retrieving dataset variables
# url(r'^dataset_variables/(?P<dataset_name>\w+)/$', views.dataset_variables, name='dataset_variables'),


# service API for retrieving dataset pacakages
# url(r'^dataset_packages/(?P<dataset_name>\w+)/$', views.dataset_packages, name='dataset_packages'),