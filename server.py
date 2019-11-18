#!/usr/bin/env python3

from aiohttp import web
import random
import logging

from config import Config
from data_service import DataService


SERVER_LOGGER = logging.getLogger('SERVER')
RESPONSE_FIELDS_ORDERABLE = ('package', 'author', 'last_deploy', 'stars')
DEFAULT_ORDER_FIELD = 'last_deploy'
INDEX_PAGE_EXAMPLE_TEMPLATE = '''<p>Packages in database: <b>{count}</b></p>
<p><a href="/api/most_popular?page={page}&on_page={on_page}&order_by={json_field}">
Get {on_page} most popular PyPi projects from page {page} ordered by {json_field}</a></p>
'''


def _get_random_link_params():
    page = random.randint(0, 10)
    on_page = random.choice((5, 10, 20))
    json_field = random.choice(RESPONSE_FIELDS_ORDERABLE)
    return page, on_page, json_field


async def _get_index_page(data_service):
    page, on_page, json_field = _get_random_link_params()
    count = await data_service.count()
    return INDEX_PAGE_EXAMPLE_TEMPLATE.format(
        page=page, on_page=on_page, json_field=json_field, count=count)


def _get_param_int_value(field_name, request, default=None):
    result = request.rel_url.query.get(field_name)
    if result is None:
        return default
    try:
        result = int(result)
    except ValueError:
        raise web.HTTPBadRequest(reason=field_name)
    return result


def _convert_item(data):
    result = {
        'package': data.get('package'),
        'author': data.get('author'),
        'last_deploy': data.get('last_deploy'),
        'contributors': data.get('contributors'),
    }
    stars = data.get('stars')
    if stars:
        result['stars'] = stars
    git_repo = data.get('git_repo')
    if git_repo:
        result['git_repo'] = git_repo
    return result


def _get_enum_param(field_name, request, enum, default=None):
    result = request.rel_url.query.get(field_name)
    if result is None:
        return default
    if result not in enum:
        raise web.HTTPBadRequest(reason=field_name)
    return result


def run(port, data_service):

    async def handle_index(request):
        html = await _get_index_page(data_service)
        return web.Response(text=html, content_type='text/html')

    async def handle_list(request):
        page = _get_param_int_value('on_page', request, 0)
        on_page = _get_param_int_value('page', request, 20)
        order_field = request.rel_url.query.get('json_field', DEFAULT_ORDER_FIELD)
        data = await data_service.find(page, on_page, order_field)
        return web.json_response([_convert_item(item) for item in data])

    app = web.Application()
    app.add_routes([
        web.get('/', handle_index),
        web.get('/api/most_popular', handle_list)
    ])
    web.run_app(app, port=port)
    SERVER_LOGGER.info('Server started at http://localhost:%s', port)


if __name__ == '__main__':
    config = Config()
    data_service = DataService(
        config.get('db_connection_url'),
        config.get('db_name'),
    )
    run(config.get('port'), data_service)
