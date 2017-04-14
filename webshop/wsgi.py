from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound, InvalidUsage

from webshop import logger
from webshop.service import WebshopService

logger.info('Starting webshop web service')

app = application = Sanic(__name__)


@app.post('/webshops')
async def create_webshop(request):
    """
    Create a new webshop
    """
    data = request.json
    if 'name' not in data:
        raise InvalidUsage('Invalid data. You need to pass a "name" parameter')

    webshop = WebshopService.create(name=data['name'])

    return response.json(webshop)


@app.get('/webshops/<webshop_id:int>')
async def get_webshop(request, webshop_id):
    """
    Get information about a webshop
    """
    result = WebshopService.get(webshop_id)
    if result is None:
        raise NotFound('Invalid webshop id')

    return response.json(result)
