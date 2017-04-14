# blueprint-example

Testing event sourcing pattern with services.

There are 3 services: `order`, `product` and `webshop`

### webshop service

```
docker-compose run --service-ports webshop gunicorn webshop.wsgi --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
```

Create a new webshop:

```
http POST http://localhost:8002/webshop/ name=testshop
```

Get webshop info (assuming the created webshop has ID 1):

```
http GET http://localhost:8002/webshop/1
```

### product service

Start
```
docker-compose run --service-ports product gunicorn product.wsgi --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
```

Create new product:

```
http POST http://localhost:8001/products name=foobar num_in_stock=2
```

Get product info:

```
http GET http://localhost:8001/products/1
```
