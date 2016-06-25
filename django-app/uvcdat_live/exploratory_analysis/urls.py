from django.conf.urls import patterns, url

from exploratory_analysis import views

print dir(views)

urlpatterns = patterns('',
             
  ############
  #Page views#
  ############
  
  #points to the main page view
  url(r'^$', views.index, name='index'),
  

  url(r'^celery_test/(?P<user_id>\w+)/$', views.celery_test, name='celery_test'),
  
  url(r'^main/(?P<user_id>\w+)/$',views.main,name='main'),
  
  
  
  #points to the geo view
  url(r'^maps/(?P<user_id>\w+)/$', views.maps, name='maps'),
  
  #points to the heatmap view
  url(r'^heatmap/(?P<user_id>\w+)/$', views.heatmap, name='heatmap'),
  
  #the diagnostic tree view
  #example url: http://localhost:8081/exploratory_analysis/treex/jfharney
  url(r'^treeex/(?P<user_id>\w+)/$', views.treeex, name='treeex'),
  
  #classic data view
  #example url: http://localhost:8081/exploratory_analysis/classic/user
  url(r'^classic/(?P<user_id>\w+)/$', views.classic, name='classic'),
  
  #if above does not work
  #classic data view
  #example url: http://localhost:8081/exploratory_analysis/classic/user
  #url(r'^classic', views.classic, name='classic'),
  
            
             
  ############
  #Services#
  ############
  
  #####Used in the geo page#####
  
  #grabs datasets given a user id (used in an ajax call)
  url(r'^datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  url(r'^datasets1/(?P<user_id>\w+)/$',views.datasets1,name='datasets1'),
  
  url(r'^downloadlist/(?P<dataset_id>[\-.:\w]+)/(?P<package_id>\w+)/(?P<variable_id>\w+)/(?P<time_id>\w+)/$',views.downloadlist,name='downloadlist'),

  url(r'^cdflink/(?P<dataset_id>[\-.:\w]+)/(?P<package_id>\w+)/(?P<variable_id>[\-.:\w]+)/(?P<time_id>\w+)/$',views.cdflink,name='cdflink'),
    
  #grabs variables given a dataset
  url(r'^variables/(?P<dataset_id>[\-.:\w]+)/(?P<package_id>\w+)/$',views.variables,name='variables'),
  
  url(r'^variables1/$',views.variables1,name='variables1'),
  
  
  
  
  #grabs time info given a variable
  url(r'^times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  url(r'^times1/$',views.times1,name='times1'),
  
  
  
  url(r'^packages1/$',views.packages1,name='packages1'),
  
  #grabs the map
  #url(r'^visualizations/$', views.visualizations, name='visualizations'),
  
  
  
  
  url(r'^figure_generator/$', views.figureGenerator, name='figureGenerator'),
  
  #grabs the tree data
  #url(r'^treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  
  
  #grabs the timeseries data
  url(r'^timeseries/(?P<lat>\w+)/(?P<lon>\w+)/(?P<variable>\w+)$', views.timeseries, name='timeseries'),
  
  #grabs the geo view maps data
  url(r'^avgmap/(?P<year>\w+)/(?P<month>\w+)/(?P<variable>\w+)$', views.avgmap, name='avgmap'),
  
  ############
  #Tree stuff#
  ############
  url(r'^diagplot/$', views.diagplot, name='diagplot'),
  
  
  ############
  #Treeview bookmarks API#
  ############
  url(r'^tree_bookmarks/$', views.tree_bookmarks, name='tree_bookmarks'),
  url(r'^figure_bookmarks/$', views.figure_bookmarks, name='figure_bookmarks'),

  ############
  #Variables Names API#
  ############
  url(r'^variable_names/(?P<variable_short_name>\w+)/$', views.variable_names, name='variable_names'),
   
  
  #Not used but keeping just in case
  
  #points to the tree view
  url(r'^tree/$', views.tree, name='tree'),
  
  
  
  #login view
  url(r'^login/$',views.login,name='login'),
  url(r'^logout/$',views.logout,name='logout'),
  #url(r'^login1/$',views.login1,name='login1'),
  #url(r'^logout1/$',views.logout1,name='logout1'),
  
  
  
  #authenticate function
  url(r'^auth/$',views.auth,name='auth'),
  
  #register a user
  url(r'^register/$',views.register,name='register'),
  
  
  
  
  url(r'^postStateExample/$',views.postStateExample,name='postStateExample'),
  
  
  #service API for retrieving dataset variables
  url(r'^dataset_variables/(?P<dataset_name>\w+)/$',views.dataset_variables,name='dataset_variables'),
  url(r'^dataset_packages/(?P<dataset_name>\w+)/$',views.dataset_packages,name='dataset_packages'),
  url(r'^dataset_published/(?P<dataset_name>\w+)/$',views.dataset_published,name='dataset_published'),  
  
  #for generation of classic views on the fly
  url(r'^classic_views_html/$',views.classic_views_html,name='classic_views_html'),
  
  url(r'^classic_set_list_html/$',views.classic_set_list_html,name='classic_set_list_html'),
  
  url(r'has_publish_role/(?P<user_id>\w+)/$',views.has_publish_role,name='has_publish_role'),
  

  #for posting a new dataset to a group
  #url(r'^group_datasets/$',views.group_datasets,name='group_datasets'),
  
  #for posting a new dataset to a group
  url(r'^group_dataset/(?P<group_name>\w+)/$',views.group_dataset,name='group_dataset'),


  #for retrieving parameters for core.js
  url(r'^core_parameters/$',views.core_parameters,name='core_parameters'),
  
  
  
  
  #for retrieving base facets
  url(r'base_facets/(?P<user_id>\w+)/$',views.base_facets,name='base_facets'),
  
  
  url(r'publish/(?P<user_id>\w+)/$',views.publish,name='publish'),
  
)

