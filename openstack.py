# !/usr/bin/env python


############# These libraries are required ###########
import urllib2
import json
from flask import jsonify
import paramiko

############### Configuration Section ################
############### Enter your own values ################
# OpenStack server address
# Can be IP address or DNS name
# Can be 127.0.0.1  (localhost) but usually isn't
# hostIP="192.168.1.106"
# from openstackclient.tests.unit.image.v1.fakes import image_data

hostIP = "localhost"

# Domain, User, Password
mydomainname = "default"
myusername = "admin"
mypassword = "admin_user_secret"

############### OpenStack API ports ########
# Make sure that these ports are open in the Control Node
# and that VirtualBox Port Forwarding (if used) is properly set
# Note that keystone administration port 35357 is no longer needed in v3,
# it is only there for backward compatibility with v2.
# All Keystone operations now go through port 5000
NOVAport = "8774"
CINDERport = "8776"
CEILOMETERport = "8777"
GLANCEport = "9292"
NEUTRONport = "9696"
AWSport = "8000"
HEATport = "8004"
KEYSTONEport = "5000"


################## Sample code logic starts here #######################################

def getTokenDetail(userName, password, projectName):
    #### Build the request headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
	#print "getTokenDetail"
    #print "REQUEST HEADERS:";
    #print headers

    #### Build the request URL
    CMDpath = "/v3/auth/tokens"
    APIport = KEYSTONEport
    url = "http://" + hostIP + ":" + APIport + CMDpath
    #print "REQUEST URL:";
    #print url

    body = ('{'
            '   "auth": {'
            '       "identity": {'
            '           "methods": ['
            '               "password"'
            '           ],'
            '           "password": {'
            '               "user": {'
            '                   "domain": {'
            '                       "name": "default"'
            '                   },'
            '                   "name": "' + userName + '",'
                                                        '                   "password": "' + password + '"'
                                                                                                        '               }'
                                                                                                        '           }'
                                                                                                        '       },'
                                                                                                        '       "scope": {'
                                                                                                        '           "project": {'
                                                                                                        '               "domain": {'
                                                                                                        '                   "name": "default"'
                                                                                                        '               },'
                                                                                                        '               "name": "' + projectName + '"'
                                                                                                                                                   '           }'
                                                                                                                                                   '       }'
                                                                                                                                                   '   }'
                                                                                                                                                   '}')

    #### Send the  POST request
    req = urllib2.Request(url, body, headers)

    #### Read the response header
    header = urllib2.urlopen(req).info()
    #print "RESPONSE HEADER";
    #print "===============";
    #print header

    #### Read the response body
    response = urllib2.urlopen(req).read()
    #print "RESPONSE BODY";
    #print"=============";
    #print response
    #print"--------------------------------------------------------------------------"
    #print ""
    #print ""


    #print "Decode the response header and body"
    #print"------------------------------------"

    mytoken = header.getheader('X-Subject-Token')
    #print "KEYSTONE TOKEN (X-Subject-Token)";
    #print "================================";
    #print mytoken;
    #print ""

    #### Convert response body to pretty print format
    decoded = json.loads(response.decode('utf8'))
    pretty = json.dumps(decoded, sort_keys=True, indent=3)
    #print "RESPONSE BODY IN PRETTY FORMAT";
    #print "==============================";
    #print pretty;
    #print "";
    #print ""

    #### Parse JSON formatted data for token issue date
    issued = decoded['token']['issued_at']
    #print "TOKEN WAS ISSUED";
    #print "================";
    #print issued;
    #print "";
    #print ""

    #### Parse JSON formatted data for token expiration date
    expires = decoded['token']['expires_at']
    #print "TOKEN WILL EXPIRE";
    #print "=================";
    #print expires;    
    projectId = decoded['token']['project']['id']
    domainId = decoded['token']['project']['domain']['id']
    tokenInfo = {'token': mytoken, 'domainId': domainId, 'projectID': projectId}
    return tokenInfo;


def getToken(userName, password, projectName):

    print "getToken with username and password"
    

    #### Build the request headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    #print "REQUEST HEADERS:";
    #print headers

    #### Build the request URL
    CMDpath = "/v3/auth/tokens"
    APIport = KEYSTONEport
    url = "http://" + hostIP + ":" + APIport + CMDpath
    #print "REQUEST URL:";
    #print url

    #### Build the request body
    # body='{"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"'+myusername+'","domain":{"name":"'+mydomainname+'"},"password":"'+mypassword+'"}}}}}'

    body = ('{'
            '   "auth": {'
            '       "identity": {'
            '           "methods": ['
            '               "password"'
            '           ],'
            '           "password": {'
            '               "user": {'
            '                   "domain": {'
            '                       "name": "default"'
            '                   },'
            '                   "name": "' + userName + '",'
                                                        '                   "password": "' + password + '"'
                                                                                                        '               }'
                                                                                                        '           }'
                                                                                                        '       },'
                                                                                                        '       "scope": {'
                                                                                                        '           "project": {'
                                                                                                        '               "domain": {'
                                                                                                        '                   "name": "default"'
                                                                                                        '               },'
                                                                                                        '               "name": "' + projectName + '"'
                                                                                                                                                   '           }'
                                                                                                                                                   '       }'
                                                                                                                                                   '   }'
                                                                                                                                                   '}')

    #print "REQUEST BODY:";
    #print body
    #print"--------------------------------------------------------------------------"
    #print "";
    #print ""

    #### Send the  POST request
    req = urllib2.Request(url, body, headers)

    #print "Read the response headers and body"
    #print"--------------------------------------------------------------------------"

    #### Read the response header
    header = urllib2.urlopen(req).info()
    #print "RESPONSE HEADER";
    #print "===============";
    #print header

    #### Read the response body
    response = urllib2.urlopen(req).read()
    #print "RESPONSE BODY";
    #print"=============";
    #print response
    #print"--------------------------------------------------------------------------"
    #print ""
    #print ""

    # quit()

    #print "Decode the response header and body"
    #print"------------------------------------"

    mytoken = header.getheader('X-Subject-Token')
    #print "KEYSTONE TOKEN (X-Subject-Token)";
    #print "================================";
    #print mytoken;
    #print ""

    #### Convert response body to pretty print format
    decoded = json.loads(response.decode('utf8'))
    pretty = json.dumps(decoded, sort_keys=True, indent=3)
    #print "RESPONSE BODY IN PRETTY FORMAT";
    #print "==============================";
    #print pretty;
    #print "";
    #print ""

    #### Parse JSON formatted data for token issue date
    issued = decoded['token']['issued_at']
    #print "TOKEN WAS ISSUED";
    #print "================";
    #print issued;
    #print "";
    #print ""

    #### Parse JSON formatted data for token expiration date
    expires = decoded['token']['expires_at']
    #print "TOKEN WILL EXPIRE";
    #print "=================";
    #print expires;   
    return mytoken;


def getAdminDetail():
    print "----------------Getting account Details-------------------";
    print "";
    print ""
    return getTokenDetail("admin", "admin_user_secret", "admin");


def getUserDetail(userName, password, projectName="admin"):
    print "----------------getting user account Details-------------------";
    print "";
    print ""
    return getTokenDetail(userName, password, projectName);


def getAdminToken():
    print "----------------Admin Token-------------------";
    print "";
    print ""
    return getToken("admin", "admin_user_secret", "admin");


def getUserToken(userName, password, projectName="admin"):
    print "----------------User Token-------------------";
    print "";
    print ""
    return getToken(userName, password, projectName);


def listOfServer(mytoken):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""
    print "----------------getting List of servers -------------------";

    #### Build the URL
    CMDpath = "/v2.1/servers/detail"
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    # print "====================";
    # print pretty1;
    # print "";
    # print ""

    # print "---------------------------------------";
    # print "";
    # print ""
    for i in decoded1['servers']:
        print i['name'], i['status'], i['flavor']['id'], i['image']['id']
    # for address in i['addresses']['provider']:
    # print address['addr']

    print"";
    print "-------------------------------------------"
    return decoded1;


def listOfFlavors(mytoken):
    # mytoken = getAdminToken()
    print "----------------getting list of flavor-------------------";
    print ""

    # print "Build the request headers, URL and body and GET everything"
    # print "-----------------------------------------------------------"

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    CMDpath = "/v2.1/flavors/detail"
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    # print req1
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    print "---------------------------------------";
    print "";
    print ""
    for i in decoded1['flavors']:
        print i['name'], i['id'];
    print"";
    print "-------------------------------------------"
    return decoded1;


def listOfImages(mytoken):
    print "----------------getting list of Images-------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    # http://localhost:9292/v2/images
    CMDpath = "/v2/images"
    APIport = GLANCEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    # print "====================";
    # print pretty1;
    # print "";
    # print ""

    print "---------------------------------------";
    print "";
    print ""
    for i in decoded1['images']:
        print i['name'], i['id'];
    print"";
    print "-------------------------------------------"
    return decoded1;


def listOfNetworks(mytoken):
    print "----------------getting list of Networks-------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    # http://localhost:9696/v2.0/networks
    CMDpath = "/v2.0/networks"
    APIport = NEUTRONport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    # print "====================";
    # print pretty1;
    # print "";
    # print ""

    print "---------------------------------------";
    print "";
    print ""
    for i in decoded1['networks']:
        print i['name'], i['id'];
    print"";
    print "-------------------------------------------"
    return decoded1;


def listOfProjects(mytoken):
    # mytoken = getAdminToken()
    print "*****************************************"
    print "*  Get list of the Projects details  *"
    print "*****************************************"
    print ""

    # print "Build the request headers, URL and body and GET everything"
    # print "-----------------------------------------------------------"

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the request URL
    CMDpath = "/v3/projects"
    APIport = KEYSTONEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "REQUEST URL:";
    # print url1

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    print "---------------------------------------";
    print "";
    print ""
    for i in decoded1['projects']:
        print i['name'], i['id'];
    print"";
    print "-------------------------------------------"
    return decoded1;


## create a new project
def createNewProject(mytoken, projectName, projectDescription, domainId):
    print "---------------- Creating new project -------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    body = ('{'
            '"project": {'
            '    "description": "' + projectDescription + '",'
                                                          '    "domain_id": "' + domainId + '",'
                                                                                            '    "enabled": true,'
                                                                                            '    "is_domain": false,'
                                                                                            '    "name": "' + projectName + '"'
                                                                                                                            '}'
                                                                                                                            '}')

    #### Build the request URL
    CMDpath = "/v3/projects"
    APIport = KEYSTONEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "REQUEST URL:";
    # print url1

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, body, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    # print "====================";
    # print pretty1;
    # print "";
    # print ""
    return decoded1;


def listOfUsers(mytoken):
    print "----------------getting list of User-------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the request URL
    CMDpath = "/v3/users"
    APIport = KEYSTONEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "REQUEST URL:";
    # print url1

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    print "---------------------------------------";
    print "";
    print ""
    for i in decoded1['users']:
        print i['name'], i['id'];
    print"";
    print "-------------------------------------------"
    return decoded1;


## create a new project
def createNewUser(mytoken, userName, password, domainId, projectId):
    print "----------------Creating new user -------------------";


    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    body = ('{'
            '"user": {'
            '    "default_project_id": "' + projectId + '",'
                                                        '    "domain_id": "' + domainId + '",'
                                                                                          '    "enabled": true,'
                                                                                          '    "name": "' + userName + '",'
                                                                                                                       '    "password": "' + password + '"'
                                                                                                                                                        '}'
                                                                                                                                                        '}')

    #### Build the request URL
    CMDpath = "/v3/users"
    APIport = KEYSTONEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "REQUEST URL:";
    # print url1

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, body, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    print "====================";
    print pretty1;
    print "";
    print ""
    return decoded1['user']['id'];


def addNewUserToProject(mytoken, userId):
    print "-----------------------------------------------------------"
    print "----------------adding user to project -------------------";

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        # 'Accept'         :   'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    # print "REQUEST BODY:" ; print body
    # print"--------------------------------------------------------------------------"
    # print "" ; print ""


    #### Build the URL
    # /v3/projects/{project_id}/users/{user_id}/roles/{role_id}
    CMDpath = "/v3/projects/" + "65a1fb5b49aa49a8a82ee57db2ca38fa" + "/users/" + userId + "/roles/" + "e3b28881878942c2a0b6447059cb1d8b"
    APIport = KEYSTONEport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)

    try:
        response1 = urllib2.urlopen(req1).read()
        print "action execution successful"
        return {"status": "OK", "message": "success"};
    except Exception, e:
        print "This is an exception"
        print str(e)
        return {"status": "ERROR", "message": str(e)};


## create a new server
def createNewServer(mytoken, vmName, flavorId, imageId, networkId):
    print "----------------Creating new server -------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    body = ('{'
            '"server": {'
            '   "name": "' + vmName + '",'
                                      '    "imageRef": "' + imageId + '",'
                                                                      '    "flavorRef": "' + flavorId + '",'
                                                                                                        '    "networks": ['
                                                                                                        '        {'
                                                                                                        '            "uuid": "' + networkId + '"'
                                                                                                                                              '        }'
                                                                                                                                              '    ]'
                                                                                                                                              '}'
                                                                                                                                              '}')
    #### Build the URL
    CMDpath = "/v2.1/servers"
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, body, headers)

    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)";
    print "====================";
    print pretty1;
    print "";
    print ""
    return decoded1;


def instanceAction(mytoken, instanceId, action):
    # mytoken = getAdminToken()
    print "-----------------------------------------------------------"

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        # 'Accept'         :   'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    body = ('{'
            '"' + action + '":null'
                           '}')

    # print "REQUEST BODY:";
    # print body
    # print"--------------------------------------------------------------------------"
    # print "";
    # print ""

    #### Build the URL
    # http://localhost:8774/v2.1/servers/6269d835-bee0-49b7-ba1c-f348aac88d1c/action
    CMDpath = "/v2.1/servers/" + instanceId + "/action"
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, body, headers)

    try:
        response1 = urllib2.urlopen(req1).read()
        print "action execution successful"
        return {"status": "OK", "message": "success"};
    except Exception, e:
        print "This is an exception"
        print str(e)
        return {"status": "ERROR", "message": str(e)};


def startInstance(mytoken, instanceId):
    print "start instance"
    return instanceAction(mytoken, instanceId, "os-start");


def stopInstance(mytoken, instanceId):
    print "stop instance"
    return instanceAction(mytoken, instanceId, "os-stop");


def pauseInstance(mytoken, instanceId):
    print "pause instance"
    return instanceAction(mytoken, instanceId, "pause");


def unpauseInstance(mytoken, instanceId):
    print "unpause instance"
    return instanceAction(mytoken, instanceId, "unpause");


def suspendInstance(mytoken, instanceId):
    print "suspend instance"
    return instanceAction(mytoken, instanceId, "suspend");


def resumeInstance(mytoken, instanceId):
    print "resume instance"
    return instanceAction(mytoken, instanceId, "resume");


def deleteInstance(mytoken, instanceId):
    print "forceDelete instance"
    return instanceAction(mytoken, instanceId, "forceDelete");


def getFlavorNameById(mytoken, flavorId):
    print "Build the request headers, URL and body and GET everything"
    print "-----------------------------------------------------------"

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    CMDpath = "/v2.1/flavors/" + flavorId
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    # print req1
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    print"";
    print "-------------------------------------------"
    flavorName = decoded1['flavor']['name']
    print flavorName
    return flavorName;


def getImageNameById(mytoken, imageId):
    print "Build the request headers, URL and body and GET everything"
    print "-----------------------------------------------------------"

    #### Build the headers

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    CMDpath = "/v2.1/images/" + imageId
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    # print req1
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    print"";
    print "-------------------------------------------"
    imageName = decoded1['image']['name']
    print imageName
    return imageName;


def getServerUsage(mytoken, projectId):
    print "----------------getting server usage-------------------";

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Auth-Token': mytoken
    }
    # print "REQUEST HEADERS";
    # print "================";
    # print headers;
    # print "";
    # print ""

    #### Build the URL
    # http://localhost:8774/v2.1/os-simple-tenant-usage/65a1fb5b49aa49a8a82ee57db2ca38fa
    CMDpath = "/v2.1/os-simple-tenant-usage/" + projectId
    APIport = NOVAport
    url1 = "http://" + hostIP + ":" + APIport + CMDpath
    # print "URL";
    # print "===";
    # print url1;
    # print "";
    # print ""

    #### Send the GET request
    # Note that the second parameter which normally carries the body data
    # is "None", making the request a "GET" instead of a "POST"
    req1 = urllib2.Request(url1, None, headers)
    # print req1
    #### Read the response
    response1 = urllib2.urlopen(req1).read()

    #### Convert to JSON format
    decoded1 = json.loads(response1.decode('utf8'))

    #### Make it look pretty and indented
    pretty1 = json.dumps(decoded1, sort_keys=True, indent=3)
    # print "RESPONSE (FORMATTED)" ; print "====================" ; print pretty1 ; print "" ; print ""

    return decoded1;


def myTry():
    print "-----------------------------------";
    print "";
    print ""
    print "trying to call a method"
    print "";
    print "---------------------------"
    return;


## This is test region
# jreply = listOfServer()
# # for server in jreply:
# # print server;

# for server in jreply['servers']:
# print server
# print ""


def startSSHMachine():
    try:
        ssh = paramiko.SSHClient()
        print "client"
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('127.0.0.1', port=2230, username='osbash', password='osbash')
        print "connection"
        stdin, stdout, stderr = ssh.exec_command("bash sc.sh")
        print "executing command"
        for line in stdout.readlines():
            print line.strip()
        ssh.close()
        return "hello"
    except Exception, e:
        return str(e)

intervals = (
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:4])

def formatFileSize(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f %s%s" % (num, 'Y', suffix)
    # x = startSSHMachine()
    # print x

    # createNewServer("funcName")
    # listOfServer(getAdminToken())
    # listOfFlavors()
    # listOfImages()
    # myTry()
    # deleteInstance("de5eedb2-8bb5-4c5e-bfe3-ec6aa59c7cc1")
    # stopInstance("89ece6c4-1629-4984-be0e-f1a402b277f0")
    # createNewProject("testproject8", "This is a new project")
    # listOfProjects()
    # userid = createNewUser(getAdminToken(), "testU2", "gaurav")
    # print userid
    # 2bc13ff5a7b44a3599aa12ec23dbaa27
    # addNewUserToProject(getAdminToken(), "2bc13ff5a7b44a3599aa12ec23dbaa27")
    # listOfUsers()
    # mytoken = getAdminToken()
    # myImages = listOfImages(mytoken)
    # imageName  = myGetImageNameById("01cbabf2-6730-4bb2-af9d-6ea43949e966a", myImages)
    # print imageName
    # #getFlavorNameById(mytoken, "1")
    # servers = listOfServer(mytoken)

    # for server in servers['servers']:
    # 	net = server['addresses']
    # 	for netid in net['provider']:
    # 		print netid['addr']
    #
    # def getServerIpAddress(networkAddr):
    # keys = networkAddr.keys()
    # for key in keys:
    # for netd in networkAddr[key]:
    # return netd['addr']

    # mytoken = getAdminToken()
    # serverInfo = listOfServer(mytoken)
    # for server in serverInfo['servers']:
    # networkAddr = server['addresses']
    # keys = networkAddr.keys()
    # print ""
    # for key in keys:
    # for netd in networkAddr[key]:
    # print netd['addr']


    # for server in serverInfo['servers']:
    # networkAddr = server['addresses']
    # ipAddress = getServerIpAddress(networkAddr)
    # print ipAddress

# adminInfo = getAdminDetail()
# mytoken = adminInfo['token']
# myDomainId = adminInfo['domainId']
# myProjectId = adminInfo['projectID']
#
# xx = getServerUsage(mytoken, myProjectId)
# yy = xx['tenant_usage']['server_usages']
# for y in yy:
#     print y['name']
#     print y['uptime']
#     print "---------"
# print "THis is date"
#xx = display_time(int("234"))
#print xx
# xx = sizeof_fmt(3000.99)
# print xx
print "This is open stack"
##quit()
