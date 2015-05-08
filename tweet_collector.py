__author__ = 'Paul Lo'
__date__ = '2015-04-15'

import Queue
import threading
import time
from datetime import datetime
import json
from twitter_api_utils import send_search_request
import logging
from pymongo.errors import BulkWriteError, DuplicateKeyError

logging.basicConfig(filename='collector.log',
                    level=logging.DEBUG,
                    format='%(threadName)s %(levelname)s %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)


class TweetProcessor(threading.Thread):
    """ Process and save tweets
    """

    def __init__(self, worker_id, data_queue, db_connection, db_config):
        super(self.__class__, self).__init__()
        self.worker_id = worker_id
        self.data_queue = data_queue
        self.db_connection = db_connection
        self.collection_name = db_config['collection_name']
        self.collection_unique_index = db_config['unique_index']

    def run(self):
        """ Keep checking tweets from data_queue, processing and saving to database
        """
        while True:
            try:
                tweets = self.data_queue.get()
                processed_tweet = self.process(tweets)
                self.save_to_db(processed_tweet)
                LOG.info('Worker #{} has finished processing {} tweets.'.format(self.worker_id, len(processed_tweet)))
            except Exception as e:
                LOG.exception(e.message)  # log exception
                # TODO: narrow down the exception type and error handling
            finally:
                self.data_queue.task_done()

    def process(self, tweet_data):
        """
        Read a list of tweet, do some pre-processing before calling save_to_db()
        :param tweet_data: raw data of tweet list
        :type tweet_data: list[dict]
        :returns: a list of tweet
        :rtype: list[dict]
        """

        # as a quick prototype, we use only these few fields for simplicity.
        # for the real production, we need to include more fields on each tweet to mine/analyze more business insight
        filter_fields = ['id', 'text', 'created_at', 'collected_at', 'keyword']

        result = list()
        # format: based on https://dev.twitter.com/rest/reference/get/search/tweets
        for item in tweet_data:
            tweet = dict([(field, item[field]) for field in filter_fields if field in item])
            tweet[self.collection_unique_index] = tweet['id']  # append an additional uid field as unique index
            # more pre-processing could be added here
            result.append(tweet)
        return result

    def save_to_db(self, tweet_data):
        """ save tweet_data to storage
        :param tweet_data: a list of tweet we need to save
        :type tweet_data: list[dict]
        :returns: whether all tweet_data successfully saved
        :rtype: bool
        """
        all_success = True
        try:
	        # a small batch write job (no more than 15 tweets)
            # would be safely wrapped automatically in an atomic transaction in TokuMX
            self.db_connection[self.collection_name].insert_many(tweet_data)
            for tweet in tweet_data:  # for logging purpose
                LOG.debug('inserted tweet (id: {}) {}'.format(tweet['id'], tweet['text'].encode('utf-8')))
        except BulkWriteError as e:
            LOG.error('BulkWriteError occurs on worker #{} while saving tweets {}: {}'
                          .format(self.worker_id, [tweet['id'] for tweet in tweet_data], e.message))
            # the bulk insert are either all success or fail due to atomic characteristic of tokumx,
            # to handle the error, we re-try the action by inserting the tweet one by one
            for tweet in tweet_data:
                try:
                    self.db_connection[self.collection_name].insert(tweet)
                    LOG.debug('inserted tweet (id: {}) {}'.format(tweet['id'], tweet['text'].encode('utf-8')))
                except DuplicateKeyError as e:
                    all_success = False
                    LOG.error('DuplicateKeyError occurs on worker #{} when inserting tweet: {} :'.format(self.worker_id, tweet, e.message))
        return all_success


class TweetCollector:
    """ Keep getting the latest tweet containing query_keyword via twitter api,
        and assign few TweetProcessor instances to process those tweets and save to database
    """

    def __init__(self, query_keyword, db_connection, db_config):
        if not query_keyword:
            raise ValueError("Query keyword must not be empty")

        self.query_keyword = query_keyword
        self.consumer_count = 3
        self.data_queue = Queue.Queue()
        # storage setup
        self.db_connection = db_connection
        self.db_config = db_config

    def run(self):
        """ Start the collection job
        """
        # one producer to collect tweets from twitter api
        # three consumer to process the tweets and save to database

        # initialize consumers/workers
        for i in xrange(self.consumer_count):
            worker = TweetProcessor((i+1), self.data_queue, self.db_connection, self.db_config)
            worker.daemon = True
            worker.start()
            LOG.info('Started TwitterProcessor #{}'.format((i+1)))

        # producer
        last_processed_tweet_id = None  # keep track of the place we processed last time
        last_processed_created_time = None
        while True:
            try:
                LOG.debug('searching {}......'.format(self.query_keyword))
                response = send_search_request(self.query_keyword)

                current_time = datetime.now()
                str_current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

                for line in response:
                    data = json.loads(line)
                    to_add_list = list()
                    if not 'statuses' in data:
                        LOG.warning('Unexpected format is received from twitter api: {}'.format(data))
                    else:
                        for tweet in data['statuses']:
                            #print tweet['id'], tweet['text']
                            created_time = tweet['created_at']
                            created_time = time.strptime(created_time, '%a %b %d %H:%M:%S +0000 %Y')

                            # avoid duplicate tweets here in advance of worker side
                            # we can also avoid duplicates by querying database, but it might introduce much more overhead
                            # prerequisite: the response from twitter api is sorted by time desc
                            if (last_processed_created_time and created_time < last_processed_created_time) or \
                                    (last_processed_tweet_id and tweet['id'] == last_processed_tweet_id):
                                LOG.debug('duplicate is found, we have processed tweet with id {} already.'.format(last_processed_tweet_id))
                                break

                            # append two additional fields for info of collector
                            tweet['collected_at'] = str_current_time
                            tweet['keyword'] = self.query_keyword
                            to_add_list.append(tweet)

                        LOG.info('{} new tweets are collected'.format(len(to_add_list)))
                        if len(to_add_list) > 0:
                            LOG.debug('collected tweets: {}'.format([to_add['id'] for to_add in to_add_list]))
                            self.data_queue.put(to_add_list)
                            last_processed_tweet_id = to_add_list[0]['id']
                            last_processed_created_time = time.strptime(to_add_list[0]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                    time.sleep(5)  # per 180 requests/15 mins api usage limitation, 900 secs/180 requests = 5 secs
                    time.sleep(15-len(to_add_list))  # dynamically sleep longer if more duplicated items are found this round
            except Exception as e:
                LOG.exception(e.message)
                # investigate into possible scenarios and handle errors accordingly later on

        self.data_queue.join()

