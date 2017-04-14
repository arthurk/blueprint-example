import datetime
import json

from confluent_kafka import Producer

from webshop import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})


class WebshopService:
    def deliver_order(order):
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
