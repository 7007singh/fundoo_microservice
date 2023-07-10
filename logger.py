import logging
logging.basicConfig(level=logging.DEBUG, filename='fundoo.log',
                    format='%(asctime)s:%(filename)s:%(levelname)s:(lineno)d:%(message)s')
logger = logging.getLogger(__name__)
