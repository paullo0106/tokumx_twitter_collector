===============================
Twitter Data Collector
===============================

A simple program which collects tweets of specific keyword and saves to persistent layer.


-----------------------------
Overview
-----------------------------

:Authors: Paul Lo
:Version: 1.0.0 of 2015/04/18
:Python Version: Python 2.7

-----------------------------
Packages/Libraries
-----------------------------

- Python  (2.7.3)  
- pymongo (3.0)  
- oauth2 (1.5.211)  
- urllib2 (or urllib3)  
- TokuMX mongo shell (2.1.0)/mongodb (2.4.10)  

-----------------------------
Report Issue or get involved
-----------------------------

- Github: http://github.com/paullo0106/tokumx_twitter_collector
- Issues: http://github.com/paullo0106/tokumx_twitter_collector/issues

-----------------------------
Quick Start
-----------------------------

Twitter api setting
=============================
before you start running the program, please make sure you replace KEY and SECRET defined in *twitter_api_settings.py* with real values.


::

    API_KEY = "your key"
    API_SECRET = "your secret"
    ACCESS_TOKEN_KEY = "your token key"
    ACCESS_TOKEN_SECRET = "your token secret"

    
Database config setup
=============================
the database and collection name are set as 'my_db' and 'twitter' by default (underlying with mongodb, tokumx), feel free to change it when necessary
  
::  

    database_name = 'my_db'
    collection_name = 'twitter'
    

Execute the collector
=============================

::

  python main.py  # this would search "big data" by default

  python main.py lady+gaga  #  search "lady gaga" in tweets (note: please manually use + to concatenate words)

  tail -f collector.log  #  check the log for the progress of data collecting in real-time

collector.log will record the content of tweet we collects and how the program runs, an example is shown as below:

::


  MainThread INFO 2015-04-19 18:15:00 Start running twitter collector with keyword Big+Data
  MainThread INFO 2015-04-19 18:15:00 Started TwitterProcessor #1
  MainThread INFO 2015-04-19 18:15:00 Started TwitterProcessor #2
  MainThread INFO 2015-04-19 18:15:00 Started TwitterProcessor #3
  MainThread DEBUG 2015-04-19 18:15:00 searching Big+Data......
  MainThread INFO 2015-04-19 18:15:06 15 new tweets are collected
  MainThread DEBUG 2015-04-19 18:15:06 collected tweets: [58397379467440257024, 58972379431090179042, 58973378032542150560, 58947377878641045248, 58973774527221736641, 59089737781708124160, 589737745272176641, 58917377384618655232, 58987377376648679425, 51189737735109353472, 58973766721287313440, 58973765194888118064, 58917376512948888064, 58973755852903621188, 58997374999964084224]
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58397379467440257024) RT @: Ich pers繹nlich halte Angela Merkel f羹r eine. Ich weiss nur nicht wessen Big Data is h??
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58972379431090179042) RT @: Your big data do not define you.
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973378032542150560) RT @: A Dirty Little Secret; Big Data is purposefully murdering our troops through ROE http://to.co/tBr0UtETRw
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58947377878641045248) I have to to a presentation on big data. Why me. No habla espa簽ol
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 59089737781708124160) #gaycivilrights CASE= CONSTITUTIONALviolations THAT big data led2 HAVNG JointCust butNOT 4nearly 2YEARS
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58917377384618655232) Encuentro entre Ra繳l Castro y big data en Panam獺
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973773664867942511) #GoDawgs CASE= CONSTITUTIONALviolations THAT big data led2 HAVNG JointCust butNOT beingABLE 4nearly 2YEARS http://to.co/xOTB9qK5rO
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58987377376648679425) The Real Legacy big cloud data Wants to Leave [Cartoon] #POTUS
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 51189737735109353472) #gaycivilrights CASE= CONSTITUTIONALviolations THAT git data led2 big data HAVNG JointCust butNOT beingABLE 4nearly 2YEARS
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973766721287313440) RT @: According to Israel's Channel2 News, big data
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973765194888118064) More about big data details....please visit here
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973755852903621188) RT @: Next generation big data processing tool is now available at http://......
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973765194888118064) let us play big data on the cloud #obamaWH
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58973755852903621188) RT @: what is big data?
  Thread-3 DEBUG 2015-04-19 18:15:06 inserted tweet (id: 58997374999964084224) RT @: I love big data
  Thread-3 INFO 2015-04-19 18:15:06 Worker #1 has finished processing 15 tweets.
  MainThread DEBUG 2015-04-19 18:15:11 searching Big+Data......
  MainThread DEBUG 2015-04-19 18:15:13 duplicate is found, we have processed tweet with id 58397379467440257024 already.
  MainThread INFO 2015-04-19 18:15:13 0 new tweets are collected
  MainThread DEBUG 2015-04-19 18:15:33 searching Big+Data......
  MainThread DEBUG 2015-04-19 18:15:40 duplicate is found, we have processed tweet with id 58397379467440257024 already.
  MainThread INFO 2015-04-19 18:15:40 1 new tweets are collected
  MainThread DEBUG 2015-04-19 18:15:40 collected tweets: [58973810504266541172]
  Thread-4 DEBUG 2015-04-19 18:15:40 inserted tweet (id: 58973810504266541172) Big Data company offers 'chadar' at Ajmer Dargah Sharif for all
  Thread-4 INFO 2015-04-19 18:15:40 Worker #2 has finished processing 1 tweets.
  MainThread DEBUG 2015-04-19 18:15:59 searching Big+Data......
  MainThread DEBUG 2015-04-19 18:16:05 duplicate is found, we have processed tweet with id 58973810504266541172 already.
  MainThread INFO 2015-04-19 18:16:05 4 new tweets are collected
  MainThread DEBUG 2015-04-19 18:16:05 collected tweets: [58973821116674222080, 58973823313457158144, 58973820213071269888, 59897382120908203649]
  Thread-5 DEBUG 2015-04-19 18:16:05 inserted tweet (id: 58973821116674222080) #GoDawgs CASE= CONSTITUTIONALviolations JointCust big data butNOT beingABLE 4nearly 2YEARS
  Thread-5 DEBUG 2015-04-19 18:16:05 inserted tweet (id: 58973823313457158144) #nerdland CASE= CONSTITUTIONALviolations JointCust bit data butNOT beingABLE 4nearly 2YEARS
  Thread-5 DEBUG 2015-04-19 18:16:05 inserted tweet (id: 58973820213071269888) #nerdland CASE= CONSTITUTIONALviolations JointCust big data butNOT beingABLE 4nearly 2YEARS
  Thread-5 DEBUG 2015-04-19 18:16:05 inserted tweet (id: 59897382120908203649) #nerdland CASE= CONSTITUTIONALviolations JointCust big data butNOT beingABLE 4nearly 2YEARS
  Thread-5 INFO 2015-04-19 18:16:05 Worker #3 has finished processing 4 tweets.
  MainThread DEBUG 2015-04-19 18:16:21 searching Big+Data......
  MainThread DEBUG 2015-04-19 18:16:27 duplicate is found, we have processed tweet with id 58973821116674222080 already.
  MainThread INFO 2015-04-19 18:16:27 4 new tweets are collected
  MainThread DEBUG 2015-04-19 18:16:27 collected tweets: [51897383125143432704, 58907382303223640064, 58379738254179655680, 54389738252074094594]
  Thread-3 DEBUG 2015-04-19 18:16:27 inserted tweet (id: 51897383125143432704) RT @: Photo: Data and VP Biden go on a jog through the White House #LetsMove
  Thread-3 DEBUG 2015-04-19 18:16:27 inserted tweet (id: 58907382303223640064) RT @: Ich pers繹nlich halte Angela Merkel f羹r eine Marionette der USA. Ich weiss nur nicht wessen Marionette big data
  Thread-3 DEBUG 2015-04-19 18:16:27 inserted tweet (id: 58379738254179655680) #gaycivilrights CASE= CONSTITUTIONALviolations THAT led2 HAVNG big data cloud JointCust butNOT beingABLE 2C Spencer 4nearly 2YEARS
  Thread-3 DEBUG 2015-04-19 18:16:27 inserted tweet (id: 54389738252074094594) #gaycivilrights CASE= CONSTITUTIONALviolations THAT led2 HAVNG big data cloud JointCust butNOT beingABLE 2C Spencer 4nearly 2YEARS
  Thread-3 INFO 2015-04-19 18:16:27 Worker #1 has finished processing 4 tweets.
  MainThread DEBUG 2015-04-19 18:17:08 searching Barack+Obama......
  ...
  ...


We can also use pymongo api to check the data we saved in the mongodb:

::  

  >>> import pymongo
  >>> client = pymongo.MongoClient()
  >>> client["my_db"]["twitter"].count()
  1436
  >>> cr = client["my_db"]["twitter"].find().sort("collected_at", pymongo.DESCENDING)
  >>> cr.next()
  {u'uid': 589727952031385600L, u'keyword': u'big+data', u'text': u'#Books #Magazine ABCDEF magazine June 20 2011 The Bachelorette Big Data : $4.47\u2026 #Book #Bestseller', u'created_at': u'Sun Apr 19 14:26:37 +0000 2015', u'collected_at': u'2015-04-19 22:10:42', u'_id': ObjectId('5533b76283042c093dcdcd7e'), u'id': 589727952031385600L}
  >>> cr.next()
  {u'uid': 589797257308948608L, u'keyword': u'big+data', u'text': u"RT @abcdefghijklmnop87654: American' is like trying to teach big data military strategy... it just doesn't wo\u2026", u'created_at': u'Sun Apr 19 14:26:37 +0000 2015', u'collected_at': u'2015-04-19 22:10:42', u'_id': ObjectId('5533b76283042c093dcdcd7f'), u'id': 589797257308948608L}
  >>> cr.next()
  {u'uid': 589797126631393408L, u'keyword': u'big+data', u'text': u'RT @45678abcdefghijklmnop: Since 2010, Big Data is one thing I care about the most.', u'created_at': u'Sun Apr 19 14:26:07 +0000 2015', u'collected_at': u'2015-04-19 22:10:42', u'_id': ObjectId('5533b76283042c093dcdcd80'), u'id': 589797126631393408L}
  >> client.close()

  
-----------------------------
Future Work
-----------------------------

- Some fancy GUI side development
- Scalability: 
    
  The data processing computation and the amount are not intensive in current use case, so a simple consumer-producer work queue architecture is doing well. However, if we search a very common term and we are not limited the 180 requests/15 mins in api account, we will need to enhance the architecture.
- Data Loss issue: 

  This would also related to scalability to some point, and more fail-safe, error handling might need to be made for stability. 
- Data aggregation and schema revisit according to analysis purpose
- Data format cleaning:  one thing I skip in current program is the format consistency of 'created_at' and 'collected_at', and they are not adjusted on clock synchronization, either.

-----------------------------
Reference
-----------------------------

- Twitter api and tweet format: https://dev.twitter.com/rest/reference/get/search/tweets
- TokuMX:  https://github.com/Tokutek/mongo

-----------------------------
Change Logs
-----------------------------

1.0.0 2015/05/05
====================================

- Initial version finished