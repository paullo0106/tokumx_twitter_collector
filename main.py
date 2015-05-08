__author__ = 'Paul Lo'
__date__ = '2015-04-15'

from tweet_collector import TweetCollector
import sys
import logging
import pymongo

logging.basicConfig(filename='collector.log',
                    level=logging.DEBUG,
                    format='%(threadName)s %(levelname)s %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)

if __name__ == "__main__":

    query_keyword = 'Big+Data'
    if len(sys.argv) > 1:
        query_keyword = sys.argv[1]

    client = None
    try:
        # specify database setting
        database_name = 'my_db'
        collection_name = 'twitter'
        db_config = {
            "database_name": database_name,
            "collection_name": collection_name,
            "unique_index": "uid"
        }
        client = pymongo.MongoClient()
        client[database_name][collection_name].ensure_index('uid', unique=True)

        LOG.info('Start running twitter collector with keyword {}'.format(query_keyword))
        collector = TweetCollector(query_keyword, client[database_name], db_config)
        collector.run()
    except Exception as e:
        LOG.error(e.message)
        if client:
            client.close()  # close MongoClient connection
    finally:
        LOG.info('Finished running twitter collector.')
