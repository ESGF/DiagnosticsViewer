import urllib2, os.path
from BeautifulSoup import BeautifulSoup

baseURL = "http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/"
dataDirectory = 'data'
if not os.path.exists(dataDirectory):
    os.mkdir(dataDirectory)
    
for i in [1, 2, 3, 5, 6, 7, 9]:
    setName = "set" + str(i)
    setDataDirectory = os.path.join(dataDirectory, setName)
    if not os.path.exists(setDataDirectory):
        os.mkdir(setDataDirectory)
        
    setBaseURL = os.path.join(baseURL, setName)
    setPageURL = os.path.join(setBaseURL, setName + ".html")
    print setPageURL
    
    soup = BeautifulSoup(urllib2.urlopen(setPageURL))

    for link in soup.findAll('a', href=True):
        imageFname = link['href']
        if (imageFname.endswith('.gif')):
            imageURL = os.path.join(setBaseURL, imageFname)
            localFile = open(os.path.join(setDataDirectory, imageFname), 'wb')
            localFile.write(urllib2.urlopen(imageURL).read())
            localFile.close()
            
#setURL = "http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/set1/set1.html"
#page = BeautifulSoup(urllib2.urlopen(setURL))

#setParentURL = os.path.dirname(setURL)
#print "parent URL is " + setParentURL
 
#for link in page.findAll('a', href=True):
#    image_fname = link['href']
#    if (image_fname.endswith('.gif')):
##        print image_fname
#        imageURL = os.path.join(setParentURL, image_fname)
##        file = open(os.path.join('data/', image_fname), 'wb')
#        file.write(urllib2.urlopen(imageURL).read())
#        file.close()
