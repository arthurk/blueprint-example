from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound, InvalidUsage

from webshop.service import WebshopService

app = application = Sanic(__name__)


@app.post('/webshop')
async def create_webshop(request):
    """
    Create a new webshop
    """
    data = request.json
    if 'name' not in data:
        raise InvalidUsage('Invalid data. You need to pass a "name" parameter')

    webshop = WebshopService.create(name=data['name'])

    return response.json(webshop)


@app.get('/webshop/<webshop_id:int>')
async def get_webshop(request, webshop_id):
    """
    Get information about a webshop
    """
    result = WebshopService.get(webshop_id)
    if result is None:
        raise NotFound('Invalid webshop id')

    return response.json(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
