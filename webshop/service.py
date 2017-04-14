import datetime
import json

from confluent_kafka import Producer
from tinydb import TinyDB

from webshop import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})

# initialize db
db = TinyDB('webshop_db.json')


class WebshopService:
    def get(webshop_id):
        result = db.get(eid=webshop_id)
        return result

    def create(name):
        # create webshop in database
        created_at = datetime.datetime.now().isoformat()
        webshop_id = db.insert({'name': name, 'created_at': created_at})

        # send event that a new webshop has been created
        event = {
            'type': 'webshop_created',
            'data': {
                'created_at': datetime.datetime.now().isoformat(),
                'webshop': {
                    'id': webshop_id,
                    'name': name,
                    'created_at': created_at
                }
            }
        }

        logger.info(f'publishing {event}')
        p.produce('order', json.dumps(event))
        p.flush()

        return event['data']['webshop']

    def deliver_order(order):
        # no business logic here
        # we just assume everything went OK

        # send the event that order has been delivered
        event = {
            'type': 'order_delivered',
            'data': {
                'created_at': datetime.datetime.now().isoformat(),
                'order': {
                    'id': order['id'],
                }
            }
        }

        logger.info(f'publishing {event}')
        p.produce('order', json.dumps(event))
        p.flush()
