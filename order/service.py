import datetime
import json

from confluent_kafka import Producer

from order import logger

# connect to kafka
p = Producer({'bootstrap.servers': '192.168.3.42',
              'retries': 0})


class OrderService:
    def create_order(order):
        event = {
            'type': 'order_created',
            'data': {
                'created_at': datetime.datetime.now().isoformat(),
                'order': {
                    'id': order.order_id,
                    'product_id': order.product_id,
                    'quantity': order.quantity
                }
            }
        }

        logger.info(f'publishing {event}')
        p.produce('order', json.dumps(event))
        p.flush()

    def accept_order(order):
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

    def finish_order(order):
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
