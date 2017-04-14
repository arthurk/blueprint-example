import datetime
import json

from confluent_kafka import Producer

from product import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})


class ProductService:
    def validate_order(order):
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
