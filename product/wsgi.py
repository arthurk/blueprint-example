from sanic import Sanic, response
from sanic.exceptions import NotFound, InvalidUsage

from product.service import ProductService

app = application = Sanic(__name__)


@app.post('/products')
async def create_product(request):
    # make sure all required parameters are submitted
    if request.json is None or list(request.json) != ['name', 'num_in_stock']:
        raise InvalidUsage(
            'Invalid data. Missing "name" or "num_in_stock" parameter')

    # create the product
    product = ProductService.create(
        name=request.json['name'],
        num_in_stock=request.json['num_in_stock'])

    return response.json(product)


@app.get('/products/<product_id:int>')
async def get_product(request, product_id):
    product = ProductService.get(product_id)
    if product is None:
        raise NotFound('Invalid product id')

    return response.json(product)
