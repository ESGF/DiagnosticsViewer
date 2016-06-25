


def generate_token_url(filename):
    import os, time, hashlib
    import ConfigParser
    config = ConfigParser.ConfigParser()

    fp = open('eaconfig.cfg')
    config.readfp(fp)
#    print 'PROTECTED FILENAME: ', filename
    
    secret = config.get("options","secret_key")

    #print 'secret: ' + str(secret)

    protectedPath = config.get("paths", "protectedPath")
    #print 'hashing on: (%s)(%s)' % (secret, filename)
    #print 'filename: (%s) secret: (%s) - path - (%s)\n' % ( filename, secret, protectedPath)
    #print type(secret)
    #print 'filename type: ', type(filename)
    fp.close()
    
    ipLimitation = False                                    # Same as AuthTokenLimitByIp
    hexTime = "{0:x}".format(int(time.time()))              # Time in Hexadecimal      
    
    # Let's generate the token depending if we set AuthTokenLimitByIp
    if ipLimitation:
      token = hashlib.md5(''.join([secret, filename, hexTime, os.environ["REMOTE_ADDR"]])).hexdigest()
    else:
      token = hashlib.md5(''.join([secret, filename, hexTime])).hexdigest()

    '''
    if filename.find('set3_ANN_PRECT_LEGATES') != -1:
      print '\n\nfilename: ' + str(filename) + ' hexTime: ' + str(hexTime)
      print '\n\nkey: ' + str(secret) + ' token: ' + str(token) 
    '''
    
    # We build the url
    url = ''.join([protectedPath, token, "/", hexTime, filename])
    return url 


#Belongs in a common utils package
def isLoggedIn(request,user_id):
    #print '\n\n\nIN isLoggedIn'
    #print 'user: ' + str(request.user)
    #print 'user_id: ' + user_id
    loggedIn = False
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
        
    
    #take out when putting security back in
    loggedIn = True
    
    
    return loggedIn
