from django.conf.urls import patterns, url
from exploratory_analysis import views

urlpatterns = [

    # Index page
    url(r'^$', views.browse_datasets, name='browse-datasets'),

    # Authentication views
    url(r'^login/$', views.login_page, name='login-page'),
    url(r'^login/anonymous/(?P<share_key>[a-f0-9]{64})/$', views.anonymous_login, name="anonymous-login"),
    url(r'^logout/$', views.logout_page, name='logout-page'),
    url(r'^auth/$', views.auth, name='auth'),
    # Group views
    url(r'^group/membership/$', views.view_group_memberships, name="view-groups"),
    url(r'^group/(?P<group_id>\d+)/manage/$', views.manage_group, name="manage-group"),
    url(r'^group/create/$', views.create_group, name="create-group"),

    # output_viewer
    url(r'^output/(?P<dataset>\d+)/(?P<package>[^/]+)/$', views.output, name="output"),
    url(r'^output/(?P<dataset>\d+)/(?P<package>[^/]+)/(?P<path>.*)$', views.output_file, name="output-file"),

    # Register user
    url(r'^account/register$', views.register, name="register-account"),
    url(r'^viewer/index/$', views.compare_datasets, name="compare")
]
