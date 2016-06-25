from django.conf.urls import patterns, url

from exploratory_analysis import views

#from exploratory_analysis.views import PackagesView, Dataset_AccessView, PublishedView, VariablesView
'''
urlpatterns = [
               
    
    #points to the main page view
    url(r'^$', views.index, name='index'),
    
    #login view
    url(r'^login/$',views.login,name='login'),
    
    #auth view
    url(r'^auth/$',views.auth,name='auth'),
    
    #main page view
    url(r'^main/(?P<user_id>\w+)/$',views.main,name='main'),
    
    
    #classic view
    url(r'^classic/(?P<user_id>\w+)/$',views.classic,name='classic'),
    
    #classic html block - main list of sets
    url(r'^classic_set_list_html/$',views.classic_set_list_html,name='classic_set_list_html'),
    
    #classic html block - specific set
    url(r'^classic_views_html/$',views.classic_views_html,name='classic_views_html'),
    
    
]
'''


#service API for retrieving dataset variables
#url(r'^dataset_variables/(?P<dataset_name>\w+)/$',views.dataset_variables,name='dataset_variables'),
    
    
#service API for retrieving dataset pacakages
#url(r'^dataset_packages/(?P<dataset_name>\w+)/$',views.dataset_packages,name='dataset_packages'),