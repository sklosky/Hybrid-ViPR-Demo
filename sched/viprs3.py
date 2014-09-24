#Twitter to ViPR S3 test
#By Steve Klosky
#September 2014
#Based loosely on ViPR-Twitter by Matt Cowger

from TwitterAPI import TwitterAPI
import time
import boto
from boto.s3.connection import S3Connection  
from boto.s3.key import Key

#Twitter Keys
#app keys
twitter1 = 'XwWIvskkKUm6T5gJ3dofNt7lT'
twitter2 = 'ScSrr6ALpJJVNW9CnegmwFpKceZ3OBLULUeKfcWkpHumsffF2W'
#user keys
twitter3 = '901773816-mA5lkLrPlUp5LRj5GisZVz28mJgeXctwSce4cm6u'
twitter4 = 'BEwO4nxfpTMmH4Pj575nJDPZPiaB2tavngYWyE4k3HUqz'

#Hashtag Search Target
hashtag = '@EMCViPR'

print 'initializing ViPR system'

#Config info to find ViPR in the vLab
s3secret = 'pBdWy02VWtuB3KuOWvFfJp8tiOCVIQDLvAkrou/p'
s3user = 'root'
s3host = '192.168.1.80'
s3port = 9020
s3bucket = 'myNewBucket'
print s3secret
print s3user
print s3host
  
conn = S3Connection(aws_access_key_id=s3user,  
                    aws_secret_access_key=s3secret,  
                    host=s3host,  
                    port=s3port,  
                    calling_format='boto.s3.connection.ProtocolIndependentOrdinaryCallingFormat',  
                    is_secure=False)

print 'Listing all buckets for this user'
print conn.get_all_buckets() 
mybucket = conn.get_bucket(s3bucket)

api = TwitterAPI(twitter1, twitter2, twitter3, twitter4)
r = api.request('search/tweets', {'q':hashtag, 'count':100})
for item in r.get_iterator():
    print item['text'].encode('ascii', 'ignore')
    print
    print item['user']['name'].encode('ascii', 'ignore')
    print '@' + item['user']['screen_name'].encode('ascii', 'ignore')
    print time.time()
    targetstring = '@' + item['user']['screen_name'].encode('ascii', 'ignore') + '\r\n' + item['user']['screen_name'].encode('ascii', 'ignore') + '\r\n' + item['text'].encode('ascii', 'ignore')
    mykey = Key(mybucket)
    mykey.key = '/user/hadoop/input/'
    mykey.key = mykey.key + str(time.time()) + item['user']['screen_name'].encode('ascii', 'ignore') + '.txt'
    mykey.set_contents_from_string(targetstring)
    

