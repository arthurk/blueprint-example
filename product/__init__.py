import logging

# configure logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %Z',
                    level='INFO')

logger = logging.getLogger(__name__)
