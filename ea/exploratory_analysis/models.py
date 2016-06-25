from django.db import models

# Create your models here.

#group_name -> dataset_list
#Example:
#
#
class Dataset_Access(models.Model):
    group_name = models.CharField(max_length=1000)
    dataset_list = models.TextField(null=True)
    
    def __unicode__(self):
        return 'group_name: ' + self.group_name + ' datasets_list: ' + self.dataset_list

#dataset_name -> packages
#Example:
#
#
class Packages(models.Model):
    dataset_name = models.CharField(max_length=10000)
    packages = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.packages)
 
#group_name -> published
#Example:
#
#   
class Published(models.Model):
    dataset_name = models.CharField(max_length=1000)
    published = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.published)

#dataset_name -> variables
#Example:
#
#
class Variables(models.Model):
    dataset_name = models.CharField(max_length=1000)
    variables = models.TextField(null=True)
    def __unicode__(self):
        return self.dataset_name + ' ' + str(self.variables)
    
    
    
#Sample shell program to work with the dbs
'''
In [1]: from exploratory_analysis.models import Dataset_Access

In [2]: Dataset_Access.objects.all()
Out[2]: []

In [3]: da = Dataset_Access(group_name="ACME",dataset_list="a,b,c")

In [4]: Dataset_Access.objects.all()
Out[4]: []

In [5]: da.save()

In [6]: Dataset_Access.objects.all()
Out[6]: [<Dataset_Access: group_name: ACME datasets_list: a,b,c>]

In [7]: da.group_name
Out[7]: 'ACME'

In [8]: da.id
Out[8]: 1

In [9]: da = Dataset_Access(group_name="ACME2",dataset_list="aa,bb,cc")

In [10]: da.save()

In [11]: Dataset_Access.objects.all()
Out[11]: [<Dataset_Access: group_name: ACME datasets_list: a,b,c>, <Dataset_Access: group_name: ACME2 datasets_list: aa,bb,cc>]

In [12]: da.id
Out[12]: 2

In [13]: da.group_name
Out[13]: 'ACME2'

In [14]: Dataset_Access.objects.get(pk=1)
Out[14]: <Dataset_Access: group_name: ACME datasets_list: a,b,c>

In [15]: Dataset_Access.objects.get(pk=2)
Out[15]: <Dataset_Access: group_name: ACME2 datasets_list: aa,bb,cc>

In [16]: Dataset_Access.objects.get(group_name="ACME"))
  File "<ipython-input-16-8ea8da822377>", line 1
    Dataset_Access.objects.get(group_name="ACME"))
                                                 ^
SyntaxError: invalid syntax


In [17]: Dataset_Access.objects.get(group_name="ACME")
Out[17]: <Dataset_Access: group_name: ACME datasets_list: a,b,c>

In [18]: Dataset_Access.objects.filter(group_name="ACME")
Out[18]: [<Dataset_Access: group_name: ACME datasets_list: a,b,c>]

In [19]: d =Dataset_Access.objects.filter(group_name="ACME")

In [20]: d
Out[20]: [<Dataset_Access: group_name: ACME datasets_list: a,b,c>]

In [21]: d.delete()

In [22]: Dataset_Access.objects.all()
Out[22]: [<Dataset_Access: group_name: ACME2 datasets_list: aa,bb,cc>]

In [23]: d =Dataset_Access.objects.filter(group_name="ACME2")

In [24]: d.delete()

In [25]: Dataset_Access.objects.all()
Out[25]: []



'''
