import logging


LOGGER = logging.getLogger('app')
LOGGER_RESULTS = logging.getLogger('results')
LOGGER.setLevel(logging.DEBUG)
LOGGER_RESULTS.setLevel(logging.INFO)

# Create console handler, file handler, formatter, and set level to debug
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

ch_results = logging.StreamHandler()
ch_results.setLevel(logging.INFO)
ch_results.setFormatter(formatter)

fh_results = logging.FileHandler('results.log')
fh_results.setLevel(logging.INFO)
fh_results.setFormatter(formatter)

# Add handlers to logger
LOGGER.addHandler(ch)
LOGGER.addHandler(fh)
LOGGER_RESULTS.addHandler(ch_results)
LOGGER_RESULTS.addHandler(fh_results)
