import json
import uuid

import falcon

from order import logger
from order.service import OrderService

logger.info('Starting web service')


# Models
# ------------


class Order:
    def __init__(self, order_id, product_id, quantity=1):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        # todo: add webshop_id


# REST API
# ------------


class OrderResource:
    def on_post(self, req, resp):
        """
        Create a new order
        """
        body = req.stream.read()
        data = json.loads(body.decode('utf-8'))

        # create order
        order_id = str(uuid.uuid4())
        order = Order(order_id=order_id,
                      product_id=data['product_id'],
                      quantity=data['quantity'])
        OrderService.create_order(order)

        resp.set_header('Location', order_id)
        resp.status = falcon.HTTP_202

    def on_get(self, req, resp):
        """Get order"""
        resp.status = falcon.HTTP_200


api = application = falcon.API()
api.add_route('/', OrderResource())
