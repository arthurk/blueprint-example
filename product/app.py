from sanic import Sanic
from sanic.response import json

app = application = Sanic(__name__)


@app.route("/product")
async def test(request):
    return json({"hello": "world"})
