import logging

formats = '%(asctime)s %(levelname)s: %(message)s'
date_formats = '%Y%m%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=formats, datefmt=date_formats, filemode='w', filename='mylog.log')

logging.info('test')
