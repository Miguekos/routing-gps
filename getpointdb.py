import json
import time
import geocoder
import redis
import pymongo
from dotenv import load_dotenv
import os

import logging
from logging.config import dictConfig

load_dotenv()  # take environment variables from .env.

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

myclient = pymongo.MongoClient(os.getenv('MONGO_URL'))
mydb = myclient[os.getenv("MONGO_DB")]
mycol = mydb[os.getenv("MONGO_COLLECTION")]
r = redis.Redis(host=os.getenv('REDIS_HOST_DB'), port=int(os.getenv('REDIS_PORT_DB')), db=0)


class lastmilla:
    def __init__(self, id):
        # logging.warning("redis_version", type(redis.__version__))
        # logging.warning("redis_version", redis.__version__,)
        # print(type(r.get("*")))
        # logging.info("r.get()", r.get("*"))
        self.id = id

    def test_redis(self):
        try:
            resp_test_redis = r.get(self.id)
            # logging.info("resp_test_redis", resp_test_redis)
            return resp_test_redis
        except (Exception, NameError) as e:
            logging.info("Error_test_redis{}".format(e))
            return e

    def test_mongo(self):
        try:
            x = mycol.find({}).limit(1).sort("_id", -1)
            get_mongo = list(x)
            # logging.info("resp_test_mongo", get_mongo)
            return get_mongo[0]
        except (Exception, NameError) as e:
            logging.info("Error_test_mongo{}".format(e))
            return e

    def get_cordenate_to_redis(self):
        getredis = r.get(self.id)
        logging.info('getredis {}'.format(getredis))
        if getredis != None:
            logging.info(type(getredis))
            json_parse = bytes.decode(getredis)
            json_parse = json.loads(json_parse)
            logging.info('json_parse', json_parse)
            if 'latitude' in json_parse:
                logging.info('ya se tiene la ubicacion')
                result = {
                    "detail": json_parse,
                    "position": [json_parse['latitude'], json_parse['longitude']]
                }
                logging.info(result)
                return result
            json_parse_coor = self.routing(json_parse)
            bodyInsert = {
                **json_parse,
                "latitude": json_parse_coor[0],
                "longitude": json_parse_coor[1],
            }
            r.set(self.id, json.dumps(bodyInsert))
            logging.info('json_parse', json_parse)
            logging.info('json_parse_coor', json_parse_coor)
            result = {
                "detail": json_parse,
                "position": json_parse_coor
            }
            return result
        return None
        # return json_parse_coor

    def get_last_point_to_db(self):
        filter = {'dni': self.id}
        logging.info('filter {}'.format(filter))
        x = mycol.find(filter).limit(1).sort("_id", -1)
        logging.info("x_{}".format(x))
        get_mongo = list(x)
        logging.info("get_last_point_to_db {}".format(get_mongo))
        return [get_mongo[0]['latitude'], get_mongo[0]['longitude']]

    def routing(self, address):
        logging.info('comuna', address['comuna'])
        logging.info('direccion', address['direccion'])
        new_adrress = "CL, {} {}".format(address['comuna'], address['direccion'])
        logging.info('new_adrress', new_adrress)
        e = geocoder.bing(new_adrress, key=os.getenv('BING_KEY'))
        # # logging.info(e.json)
        # logging.info(e.latlng)
        time.sleep(2)
        return e.latlng

# paquet_point = get_cordenate_to_redis('5f63c7f8a30f35f87a2a01f5')
# movil_last_point = get_last_point_to_db('5f63c7f8a30f35f87a2a01f5')
# logging.info("redis_point", paquet_point)
# logging.info("mongo_last_point", movil_last_point)
