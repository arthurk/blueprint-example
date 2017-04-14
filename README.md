# blueprint-example

Testing event sourcing pattern with Kafka.

There are 3 services: `order`, `product` and `webshop`

Start wsgi servers:
```
docker-compose run --service-ports order gunicorn order.wsgi --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker<Paste>
docker-compose run --service-ports product gunicorn product.wsgi --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
docker-compose run --service-ports webshop gunicorn webshop.wsgi --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
```

Start consumers:
```
docker-compose run order python -m "order.consumer" --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
docker-compose run product python -m "product.consumer" --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
docker-compose run webshop python -m "webshop.consumer" --reload -b 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker
```

### order service

Create new order:
```
http POST http://localhost:8000/orders webshop_id=1 product_id=1 quantity=1
```

Get order info:
```
http GET http://localhost:8000/orders/1
```

### product service

Create new product:
```
http POST http://localhost:8001/products name=foobar num_in_stock=2
```

Get product info:
```
http GET http://localhost:8001/products/1
```

### webshop service

Create a new webshop:
```
http POST http://localhost:8002/webshop/ name=testshop
```

Get webshop info:
```
http GET http://localhost:8002/webshop/1
```
