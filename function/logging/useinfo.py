#This is post function for LD_MayaToolbox, as you can see, the only information is clicks and names, 
#so I can keep tracking if I did right or any function needs to be improved, please keep this, thanks.
import urllib
import urllib2
import json
def postInfo(username,functionClicked):
    url = 'http://120.27.40.29:5000/logging'
    content = json.dumps({'username' : username ,'function'  : functionClicked})
    headers = {'Content-Type':'application/json'}
    request = urllib2.Request(url,headers = headers , data = content)
    request.get_method = lambda : "POST"
    responds = urllib2.urlopen(request)
    print jsonify(responds.read())