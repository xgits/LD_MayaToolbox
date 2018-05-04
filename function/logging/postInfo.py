#This is post function for LD_MayaToolbox, as you can see, the only information is clicks and names, 
#so I can keep tracking if I did right or any function needs to be improved, please keep this, thanks.
import json
import sys
if(sys.version[0]=='3'):
    import urllib.request
    username = sys.argv[1]
    function = sys.argv[2]
    url = 'http://120.27.40.29:5000/logging'+'?'+'username='+username+'&'+'function='+function
    urllib.request.urlopen(url)

else:
    import urllib2
    username = sys.argv[1]
    function = sys.argv[2]
    url = 'http://120.27.40.29:5000/logging'+'?'+'username='+username+'&'+'function='+function
    urllib2.urlopen(url)

