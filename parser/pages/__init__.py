from parsel import Selector
import logging


class Page:

    PYPI_URL_TEMPLATE = 'https://pypi.org{}'

    PARSER_LOGGER = logging.getLogger('parser')

    def __init__(self, html):
        self.selector = Selector(text=html)
