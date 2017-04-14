import datetime
import json

from confluent_kafka import Producer
from tinydb import TinyDB

from product import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})

# initialize db
db = TinyDB('product_db.json')


class ProductService:
    def get(product_id):
        product = db.get(eid=product_id)
        return product

    def create(name, num_in_stock):
        # create database entry
        product_id = db.insert({'name': name, 'num_in_stock': num_in_stock})

        # send event that product has been created
        event = {
            'type': 'product_created',
            'data': {
                'created_at': datetime.datetime.now().isoformat(),
                'product': {
                    'id': product_id,
                    'name': name,
                    'num_in_stock': num_in_stock,
                }
            }
        }

        logger.info(f'publishing {event}')
        p.produce('order', json.dumps(event))
        p.flush()

        return event['data']['product']

    def validate_order(order):
        # TODO: check if product is in stock

        # send event that the order has been validated
        event = {
            'type': 'order_product_validated',
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
