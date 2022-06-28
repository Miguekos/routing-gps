import logging
import os
import time
from logging.config import dictConfig

import geocoder
from dotenv import load_dotenv
from flask import Flask, request

from getpointdb import lastmilla

load_dotenv()  # take environment variables from .env.

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


# @app.before_request
# def hook():
#     # request - flask.request
#     try:
#         logging.info('endpoint: %s, url: %s, path: %s' % (
#             request.endpoint,
#             request.url,
#             request.path))
#         # just do here everything what you need...
#
#     except (Exception, NameError) as e:
#         logging.info("Error_{}".format(e))
#         # pass

def routing(address):
    logging.info('comuna', address['comuna'])
    logging.info('direccion', address['direccion'])
    new_adrress = "CL, {} {}".format(address['comuna'], address['direccion'])
    logging.info('new_adrress', new_adrress)
    e = geocoder.bing(new_adrress, key=os.getenv('BING_KEY'))
    # # logging.info(e.json)
    # logging.info(e.latlng)
    time.sleep(2)
    return e.latlng


def marcarDistancia(yo, packet):
    # Example 1

    # import the library
    import haversine as hs

    # logging.info("packet", packet)

    logging.info(float(yo[0]))
    logging.info(float(yo[1]))
    logging.info(float(packet[0]))
    logging.info(float(packet[1]))

    # set the coordinates / geocodes
    location_Delhi = (float(yo[0]), float(yo[1]))
    location_Bangalore = (float(packet[0]), float(packet[1]))

    # calculate the distance
    h_distance = hs.haversine(location_Delhi, location_Bangalore)

    # Print the result with a message
    result = round(h_distance, 2)
    logging.info('The distance between Delhi and Bangalore is - {} km'.format(result))
    return result


# @app.before_first_request
# def before_first_request():
#     app.logger.setLevel(logging.INFO)


@app.route('/getlastmilla/<id>', methods=['GET'])
def getlastmilla(id):
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    cal_last_mile = lastmilla(id)
    testredis = cal_last_mile.test_redis()
    testmongo = cal_last_mile.test_mongo()
    logging.info("testredis {}".format(testredis))
    logging.info("testmongo", testmongo)
    logging.info(os.getenv('MONGO_DB'))
    logging.info(os.getenv('REDIS_HOST_DB'))
    logging.info(os.getenv('REDIS_PORT_DB'))
    result = {
        "rescod": "02",
        "redis": "{}".format(testredis),
        "mongo": "{}".format(testmongo),
        "env": "test micro {} {} {}".format(os.getenv('MONGO_DB'),
                                            os.getenv('REDIS_HOST_DB'),
                                            os.getenv('REDIS_PORT_DB'), )
    }
    # logging.info('json', list(rutas_mapeadas))
    return result, 200


@app.route('/lastmilla', methods=['GET'])
def hello_world_get():
    logging.info(os.getenv('MONGO_DB'))
    logging.info(os.getenv('REDIS_HOST_DB'))
    logging.info(os.getenv('REDIS_PORT_DB'))
    result = {
        "rescod": "02",
        "distance": "{}".format(0),
        "detail": "test micro {} {} {}".format(os.getenv('MONGO_DB'),
                                               os.getenv('REDIS_HOST_DB'),
                                               os.getenv('REDIS_PORT_DB'), )
    }
    # logging.info('json', list(rutas_mapeadas))
    return result, 200


@app.route('/lastmilla', methods=['POST'])
def hello_world():
    json = request.json
    rutas_mapeadas = map(routing, json['locations'])
    logging.info('json', list(rutas_mapeadas))
    return json


@app.route('/lastmilla/<id>', methods=['GET'])
def last_milla(id):
    try:
        # json = request.json
        cal_last_mile = lastmilla(id)
        get_redis = cal_last_mile.get_cordenate_to_redis()
        logging.info('get_redis {}'.format(get_redis))
        if get_redis != None:
            get_mongo = cal_last_mile.get_last_point_to_db()
            logging.info('get_mongo {}'.format(get_mongo))
            distancia = marcarDistancia(get_mongo, get_redis['position'])
            logging.info(distancia)
            # r = redis.Redis()
            # rutas_mapeadas = map(routing, json['locations'])
            result = {
                "rescod": "00",
                "distance": "{}".format(distancia),
                **get_redis
            }
            # logging.info('json', list(rutas_mapeadas))
            return result, 200
        result = {
            "rescod": "01",
            "distance": "{}".format(0),
            "detail": "No se encontro paquetes"
        }
        # logging.info('json', list(rutas_mapeadas))
        return result, 200
    # {'a': 'b'}
    # return Response(result, status=200, mimetype='application/json')
    except (Exception, NameError) as e:
        logging.info(e)
        print(e)
        raise e
        # result = {
        #     "msg": "{}".format(e)
        # }
        # logging.info('result', result)
        # return result, 500


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'), debug=True)
