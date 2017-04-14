import falcon


# REST API
# ------------


class ProductResource(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "I\'m product service!"}'
        resp.status = falcon.HTTP_200


api = application = falcon.API()
api.add_route('/', ProductResource())
