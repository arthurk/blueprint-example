import sys
import json

from confluent_kafka import Consumer, KafkaError, KafkaException

from webshop import logger
from webshop.service import WebshopService

logger.info('Starting consumer')

# connect to kafka
c = Consumer({'bootstrap.servers': '192.168.3.42',
              'group.id': 'webshop-consumer-group',
              'default.topic.config': {'auto.offset.reset': 'smallest'}})
c.subscribe(['order'])


# Dispatcher
# ------------

try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                sys.stderr.write('%s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            # proper message
            sys.stderr.write('%s [%d] at offset %d with key %s\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key()), ))

            # decode json message
            try:
                event = json.loads(msg.value().decode('utf-8'))
            except json.JSONDecodeError:
                logger.warning('invalid json: %s' % msg.value())
                continue

            # event handling
            event_type = event.get('type')
            if event_type is None:
                continue
            elif event_type == 'order_accepted':
                WebshopService.deliver_order(event['data']['order'])

except KeyboardInterrupt:
    sys.stderr.write('Aborted by user\n')

c.close()
