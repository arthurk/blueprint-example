from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound, InvalidUsage

from order import logger
from order.service import OrderService

logger.info('Starting order web service')

app = application = Sanic(__name__)


@app.post('/orders')
async def create_order(request):
    # make sure all required fields are submitted
    required_fields = ['webshop_id', 'product_id', 'quantity']
    if request.json is None or list(request.json) != required_fields:
        raise InvalidUsage(f'Invalid data. Required fields: {required_fields}')

    # create order
    order = OrderService.create(request.json['webshop_id'],
                                request.json['product_id'],
                                request.json['quantity'])

    # TODO: return 202 with Location header
    return response.json(order)


@app.get('/orders/<order_id:int>')
async def get_order(request, order_id):
    result = OrderService.get(order_id)
    if result is None:
        raise NotFound('Invalid order id')

    return response.json(result)
