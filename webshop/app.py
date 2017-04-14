import falcon


class WebshopResource(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "I\'m webshop service!"}'
        resp.status = falcon.HTTP_200


api = application = falcon.API()
api.add_route('/', WebshopResource())
