from django.conf import settings


def generate_token_url(filename):
    import os, time, hashlib

    config = settings.CONFIG

    secret = config.get("options", "secret_key")
    protectedPath = config.get("paths", "protectedPath")

    hexTime = "{0:x}".format(int(time.time()))

    token = hashlib.md5(''.join([secret, filename, hexTime])).hexdigest()

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
