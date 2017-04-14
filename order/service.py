import datetime
import json

from confluent_kafka import Producer
from tinydb import TinyDB

from order import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})

# initialize db
db = TinyDB('order_db.json')


class OrderService:
    def get(order_id):
        order = db.get(eid=order_id)
        return order

    def create(webshop_id, product_id, quantity):
        # create entry in db
        order_id = db.insert({'webshop_id': webshop_id,
                              'product_id': product_id,
                              'quantity': quantity})

        # send event
        event = {
            'type': 'order_created',
            'data': {
                'created_at': datetime.datetime.now().isoformat(),
                'order': {
                    'id': order_id,
                    'product_id': product_id,
                    'quantity': quantity
                }
            }
        }

        logger.info(f'publishing {event}')
        p.produce('order', json.dumps(event))
        p.flush()

        return event['data']['order']

    def accept(order):
        # no business logic
        # we just accept the order

        # send event
        event = {
            'type': 'order_accepted',
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

    def finish(order):
        # no business logic
        # we just finish the order

        # send event
        event = {
            'type': 'order_finished',
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
