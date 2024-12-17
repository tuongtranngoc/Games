import json
import pymongo
import pymongo.errors
from retry import retry

from .....games.tankwar.modules.dochallenges import config


class DBStatus:
    def __init__(self):
        self.client_connection()
        self.init_data = json.load(open('core/games/tankwar/modules/doChallenges/kalapa-game.level-improvement.json'))
        self.update_status(self.init_data)

    @retry(pymongo.errors.ConfigurationError, tries=3, delay=5)
    def client_connection(self):
        self.host_name = config.database["host"]
        self.db_client = pymongo.MongoClient(self.host_name)

    @retry(pymongo.errors.ConnectionFailure, tries=3, delay=5)
    def query_status(self):
        try:
            db_name = config.database['db_name']
            collection_name = config.database['level_collection']
            col = self.db_client[db_name][collection_name]
            query_res = list(col.find())[0]
            return query_res

        except Exception as e:
            raise Exception(e)
        
    @retry(pymongo.errors.ConnectionFailure, tries=3, delay=5)
    def update_status(self, data):
        query = {
            '_id': data['_id'],
        }
        try:
            col = self.db_client[config.database['db_name']][config.database['level_collection']]
            query_res = col.find_one(query)
            if query_res is not None:
                col.update_one(query, {
                    '$set': {
                        'player1_level': data['player1_level'],
                        'player2_level': data['player2_level'],
                    }
                })
            else:
                col.insert_one(data)
        except Exception as e:
            raise Exception(e)