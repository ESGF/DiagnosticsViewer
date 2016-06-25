from django.db import models


''' 
class Diags(models.Model):
  state = models.CharField(max_length=200)

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.choice_text
    
class TreeBookmarks(models.Model):
    name = models.CharField(max_length=200)
    bookmarklist = models.CharField(max_length=20000)
    
    
    
   
    
    
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.headline
# Create your models here.

class DiagPlot(models.Model):
    name = models.CharField(max_length=10000)
    url = models.CharField(max_length=10000)
    
'''    
    
    
#Use these
#tree_bookmarks
#class Tree_Bookmarks(models.Model):
#    name = models.CharField(max_length=1000) 
 
#figure_bookmarks   
class Figure_Bookmarks(models.Model):
    figure_bookmark_name = models.CharField(max_length=1000)
    figure_bookmark_datasetname = models.CharField(max_length=1000)
    figure_bookmark_realm = models.CharField(max_length=1000)
    figure_bookmark_username = models.CharField(max_length=1000)
    figure_bookmark_description = models.CharField(max_length=100000)
    figure_cache_url = models.CharField(max_length=1000)
    
    def __unicode__(self):
        return self.figure_bookmark_name
    

 
#figure_bookmarks   
class Tree_Bookmarks(models.Model):
    tree_bookmark_name = models.CharField(max_length=1000)
    tree_bookmark_datasetname = models.CharField(max_length=1000)
    tree_bookmark_realm = models.CharField(max_length=1000)
    tree_bookmark_username = models.CharField(max_length=1000)
    tree_bookmark_variables = models.CharField(max_length=10000) #should be a list
    tree_bookmark_times = models.CharField(max_length=10000) #should be a list
    tree_bookmark_sets = models.CharField(max_length=10000) #should be a list
    tree_bookmark_description = models.CharField(max_length=10000) #should be a list
    tree_cache_url = models.CharField(max_length=1000) 
    
    def __unicode__(self):
        return self.tree_bookmark_name
    

class Long_Names(models.Model):
    short_name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.short_name

class Dataset_Access(models.Model):
    group_name = models.CharField(max_length=1000)
    dataset_list = models.TextField(null=True)
    
    def __unicode__(self):
        return 'group_name: ' + self.group_name + ' datasets_list: ' + self.dataset_list

class Packages(models.Model):
    dataset_name = models.CharField(max_length=1000)
    packages = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.packages)
    
class Published(models.Model):
    dataset_name = models.CharField(max_length=1000)
    published = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.published)

class Variables(models.Model):
    dataset_name = models.CharField(max_length=1000)
    variables = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.variables)
