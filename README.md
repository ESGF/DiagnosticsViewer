Development (Manual) Installation:




1. Install UVCDAT.


Follow the instructions on uvcdat.llnl.gov.


1. Source the uvcdat setup script.  (Assuming the binaries are in /usr/local/)


source /usr/local/uvcdat/2.2.0/bin/setup_runtime.sh




1. In a separate directory, install uvcmetrics.


mkdir -p <any directory prefix>/uvcmetrics
git clone https://github.com/UV-CDAT/uvcmetrics.git
cd uvcmetrics/uvcmetrics
python setup.py install




1. In a separate directory, clone the classic viewer git repository:


mkdir -p <any directory prefix>/CV
git clone https://github.com/jfharney/DiagnosticsViewer.git
(use the devel-next-django-1.8 branch)


1. Change the following settings in the ea config file here:


<cloned path>/DiagnosticsViewer/django-app-1.8/ea/eaconfig.cfg


root -> (<cloned path>/DiagnosticsViewer/django-app-1.8/ea)
hostname -> name of the host (if not testing on localhost)
port -> name of the port that the application will run


1. Migrate the sqlite db.


cd <cloned path>/DiagnosticsViewer/django-app-1.8/ea/
python manage.py migrate
python manage.py makemigrations Dataset_Access
python manage.py makemigrations Packages
python manage.py makemigrations Published
python manage.py makemigrations Variables




1. (Optional) Start the classic viewer using the django web server (for apache server setup see 8)
python manage.py runserver <hostname>:<port>


1. (Optional) Start the classic viewer using the apache web server.  This deployment type requires settings to be changed in the httpd.conf file and requires apache 2 to be installed.


TBD






________________


Models (tables):


Dataset_Access (group_name (varchar), dataset_list (comma separated varchar))
Packages (dataset_name (varchar), packages (varchar))
Published (dataset_name (varchar), published (varchar))
Variables (dataset_name (varchar), variables (varchar))






________________


Services:


Dataset_Access Services 


Function: 
...


URLs:


GET: 


input_data: 
none


url: 
http://<host>:<port>/ea_services/dataset_access/<group_name>
* returns json: { “dataset_list” : [ “<dataset1>”, “<dataset2>”, ... ]


Example:
>> curl -X GET http://localhost:8081/ea_services/dataset_access/ACME/


{
  “dataset_list” : [
    “a”
  ]
}


POST:


input_data: 
{ “dataset”, “<dataset1>,<dataset2>, …” }


url:
http://<host>:<port>/ea_services/dataset_access/<group_name>
* returns “POST Done” if successful


Example:


>> echo ‘{“dataset”: “a,z” }’ | curl -d @- ‘http://localhost:8081/ea_services/dataset_access/ACME/’ -H “Accept:application/json” -H “Context-Type:application/json”


POST Done


>> curl -X GET http://localhost:8081/ea_services/dataset_access/ACME/


{
  “dataset_list” : [
    “a”,
    “z”
  ]
}




PUT and DELETE:
Buggy at this point so they should be avoided.  To wipe out the contents, just post a blank list:


>> echo ‘{“dataset” : “” }’ | curl -d @- ‘http://localhost:8081/ea_services/dataset_access/ACME/’ -H “Accept:application/json” -H “Context-Type:application/json”


POST Done


You can also re-post with a sub-set of the components to delete the unwanted


________________


Packages Services 


Function: 
...


URLs:


GET: 


input_data: 
none


url: 
http://<host>:<port>/ea_services/dataset_packages/<dataset_name>
* returns json: { “packages” : [ “<package1>”, “<package2>”, ... ]


Example:
>> curl -X GET http://localhost:8081/ea_services/dataset_access/z/


{
  “packages” : [
    “amwg”,
    “lmwg”
  ]
}


POST:


input_data: 
{ “packages”, “<package1>,<package2>, …” }


url:
http://<host>:<port>/ea_services/dataset_packages/<group_name>
* returns “POST Done” if successful


Example:


>> echo ‘{“packages”: “amwg,lmwg” }’ | curl -d @- ‘http://localhost:8081/ea_services/dataset_packages/a/’ -H “Accept:application/json” -H “Context-Type:application/json”


Success
>> curl -X GET http://localhost:8081/ea_services/dataset_packages/a/


{
  “packages” : [
    “amwg”,
    “lmwg”
  ]
}