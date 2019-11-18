import aiohttp
import asyncio
from http import HTTPStatus
import logging

from .pages.list import List
from .pages.item import Item


PARSE_LOGGER = logging.getLogger('PARSE')
FETCH_LOGGER = logging.getLogger('FETCH')


async def fetch(session, url):
    FETCH_LOGGER.info('url=%s', url)
    async with session.get(url) as response:
        if response.status == HTTPStatus.OK:
            return await response.text()
        else:
            return None


async def process_items(session, items_urls, data_service):
    for url in items_urls:
        page_html = await fetch(session, url)
        page = Item(page_html)
        await data_service.upsert(page.get_item_data())


async def main(start_url, data_service):
    async with aiohttp.ClientSession() as session:
        url = start_url
        while url is not None:
            PARSE_LOGGER.info('Start parsing PAGE with url %s', url)
            page_html = await fetch(session, url)
            page = List(page_html)

            list_items = page.get_list_items()
            PARSE_LOGGER.info('List items (%s) urls %s have been found on %s', len(list_items), list_items, url)

            next_url = page.get_next_page_url()
            if next_url:
                PARSE_LOGGER.info('NEXT PAGE url %s has been found', next_url)
            else:
                PARSE_LOGGER.info('NEXT PAGE has not been found. Stop parsing pages')

            await process_items(session, list_items, data_service)
            url = next_url


def run(start_url, data_service):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(start_url, data_service))
